import os
import json
import shutil
import requests
import mimetypes
import subprocess
from description_indexer.dao_plugins import DaoSystem
from description_indexer.models.description import DigitalObject, FileVersion

from urllib.request import urlopen
import cgi

class Hyrax(DaoSystem):
	dao_system_name = "hyrax"


	def __init__(self):
		print (f"Setup {self.dao_system_name} dao system for reading digital object data.")
		
		check_java = subprocess.Popen(["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = check_java.communicate()
		if check_java.returncode != 0:
			raise Exception("Unable to access Java")

		# requires tika-app.jar file in $TIKA_PATH
		if os.name == "nt":
			# tika uses native encoding grrr
			self.tika_encoding = "Windows-1252"
		else:
			self.tika_encoding = "utf-8"
		self.tika_path = "\"" + str(os.path.join(os.environ.get("TIKA_PATH"), "tika-app.jar")) + "\""

		self.tika_priorities = (".docx", ".pptx", ".xlsx", ".doc", ".ppt", ".xls", ".pdf")

	def get_mime_type(self, filename):

		docmimes = {
			".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
			".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
			".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation"
			}

		mimetype = mimetypes.MimeTypes().guess_type(filename)[0]
		if mimetype == None:
			for key in docmimes:
				if filename.lower().endswith(key):
					mimetype = docmimes[key]
		if mimetype == None:
			raise Exception("Failed to get mimetype.")

		return mimetype

	def read_data(self, component, quick=None):

		only_dao = False
		if len(component.digital_objects) == 1:
			only_dao = True

		for dao in component.digital_objects:

			# in all but a few cases, UA's ASpace file versions actually hold digital object URIs
			fv_count = 0
			for fv in dao.file_versions:
				fv_count += 1
			if fv_count == 1:
				dao.uri = dao.file_versions[0].href.strip()
			else:
				raise Exception ("ASpace DAO unexpectedly has multiple file versions! --> " + str(dao.uri))			

			dao.metadata = {}
			print ("reading data from " + dao.uri + "?format=json")
			if dao.uri.startswith("https://archives.albany.edu/catalog?f%5Barchivesspace_record_tesim"):
				print (dao.uri)
				record_json = requests.get(dao.uri + "?format=json").json()
			elif dao.uri.startswith("https://web.archive.org/web"):
				print (dao.uri)
				record_json = requests.get(dao.uri + "?format=json").json()
			else:
				record_json = requests.get(dao.uri + "?format=json").json()

			# In cases where there's only one DO, in local practice, it's representative unless its set as "part"
			if only_dao:
				if "coverage" in record_json.keys() and record_json["coverage"] == "part":
					dao.is_representative = "false"
				else:
					dao.is_representative = "true"

			dao.identifier = record_json['id']
			metadata_fields = {
							 "date_uploaded": "date_uploaded",
							 "date_modified": "date_modified",
							 "accession": "accession", 
							 "resource_type": "type", 
							 "processing_activity": "processing_activity",
							 "coverage": "coverage",
							 "extent": "extent",
							 #"date_created": "date",
							 "creator": "creator",
							 "contributor": "contributor",
							 "description": "description",
							 "abstract": "abstract",
							 "keyword": "keyword",
							 "language": "language",
							 "physical_dimensions": "physical_dimensions",
							 "master_format": "preservation_format",
							 "date_digitized": "date_digitized",
							 "identifier": "legacy_identifier",
							 "source": "original_format"
							 }

			for field in metadata_fields.keys():
				if field in record_json.keys() and record_json[field] and len(record_json[field]) > 0:
					dao.metadata[metadata_fields[field]] = record_json[field]

			# This overrides the ASpace Digital Object Label with the title in Hyrax
			if len(record_json['title']) > 0:
				dao.label = record_json['title'][0]

			# set subjects
			dao_subjects = []
			if len(record_json['subject']) > 0:
				dao_subjects.extend(record_json['subject'])
			dao.subjects = dao_subjects
			
			# Licence or rights
			if len(record_json['license']) > 0:
				dao.rights_statement = record_json['license'][0]
			elif len(record_json['rights_statement']) > 0:
				dao.rights_statement = record_json['rights_statement'][0]
			else:
				dao.rights_statement = "https://creativecommons.org/licenses/by-nc-nd/4.0/"

			# Parse the jsonld to get the full list of file objects
			jsonld = requests.get(dao.uri + "?format=jsonld").json()
			file_objects = []
			mimes = []
			extentions = []
			for fileObject in jsonld["@graph"]:
				if "ore:proxyFor" in fileObject.keys():
					fileSetID = fileObject["ore:proxyFor"]["@id"].split("archives.albany.edu/catalog/")[1]
					fileObjectURL = "https://archives.albany.edu/downloads/" + fileSetID
					# Gotta get the filename from Content-Disposition for mimetype :(
					remotefile = urlopen(fileObjectURL)
					content_data = remotefile.info()['Content-Disposition']
					value, params = cgi.parse_header(content_data)			
					fileObjectName = params["filename"]
					fileObjectMimetype = self.get_mime_type(fileObjectName)
					file_object = {}
					file_object["url"] = fileObjectURL
					file_object["name"] = fileObjectName
					file_object["mime"] = fileObjectMimetype
					file_object["ext"] = os.path.splitext(fileObjectName)[1].lower()
					mimes.append(fileObjectMimetype)
					extentions.append(os.path.splitext(fileObjectName)[1].lower())
					file_objects.append(file_object)

			dao.thumbnail_href = file_objects[0]["url"] + "?file=thumbnail"
			if len(file_objects) == 1:
				dao.metadata["filename"] = file_objects[0]["name"]

			#these are really Components or aggregages of DOs currently managed in Hyrax
			rights = dao.rights_statement
			metadata = dao.metadata
			subjects = dao.subjects
			dao_id = dao.identifier
			dao_uri = dao.uri
			if len(set(mimes)) > 1 or mimes[0].lower().startswith("image"):
				#multiformat or aggregate of images
				component.digital_objects = []
				if len(set(mimes)) == 1:
					component.iiif_manifest = dao_uri + "/manifest"
				fo_count = 0
				for file_object in file_objects:
					fo_count += 1
					do = DigitalObject()
					do.uri = f"https://archives.albany.edu/concern/parent/{dao_uri.rsplit('/', 1)[1]}/file_sets/{file_object['url'].split('/downloads/')[1]}"
					do.label = file_object["name"]
					do.identifier = dao_id + "-" + str(fo_count)
					do.is_representative = "false"
					do.thumbnail_href = file_object["url"] + "?file=thumbnail"
					do.rights_statement = rights
					do.metadata = metadata
					do.subjects = subjects
					fv = FileVersion()
					fv.href = file_object["url"]
					fv.is_access = "true"
					fv.filename = file_object["name"]
					fv.mime_type = file_object["mime"]
					do.file_versions.append(fv)
					component.digital_objects.append(do)

			else:
				# single digital objects with multiple versions

				original_exts = [".pdf", ".csv"]
				office_docs = [".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt"]
				audio_exts = [".mp3"]
				video_exts = [".mpg", ".mp4", ".mov", ".avi"]

				if len(file_objects) > 1:
					raise Exception("Unexpected multiple file versions for: " + dao.url)

				if len(set(extentions)) > 1:
					raise Exception("Unexpectedly discovered multiple file extentions for " + dao.url)
				ext = extentions[0]
				if ext in office_docs:
					original = FileVersion()
					original.href = file_objects[0]["url"]
					original.is_original = "true"
					original.is_access = "false"
					original.filename = file_objects[0]["name"]
					original.mime_type = file_objects[0]["mime"]
					pdf = FileVersion()
					pdf.href = file_objects[0]["url"] + "?file=pdf"
					pdf.is_access = "true"
					pdf.label = "PDF"
					pdf.filename = os.path.splitext(file_objects[0]["name"])[0] + ".pdf"
					pdf.mime_type = "application/pdf"
					if ext == ".docx" or ext == ".doc":
						original.label = "Word Document (original)"
					elif ext == ".xlsx" or ext == ".xls":
						original.label = "Spreadsheet (original)"
					elif ext == ".pptx" or ext == ".ppt":
						original.label = "Powerpoint (original)"
					dao.file_versions = []
					dao.file_versions.append(original)
					dao.file_versions.append(pdf)
				elif ext in audio_exts:
					mp3 = FileVersion()
					mp3.href = file_objects[0]["url"] + "?file=mp3"
					mp3.label = "MP3"
					mp3.filename = file_objects[0]["name"]
					mp3.mime_type = file_objects[0]["mime"]
					ogg = FileVersion()
					ogg.href = file_objects[0]["url"] + "?file=ogg"
					ogg.is_access = "true"
					ogg.label = "Ogg"
					ogg.filename = os.path.splitext(file_objects[0]["name"])[0] + ".ogg"
					ogg.mime_type = "audio/ogg"
					dao.file_versions = []
					dao.file_versions.append(mp3)
					dao.file_versions.append(ogg)
				elif ext in video_exts:
					original = FileVersion()
					original.href = file_objects[0]["url"]
					original.label = "Original"
					original.filename = file_objects[0]["name"]
					original.mime_type = file_objects[0]["mime"]
					webm = FileVersion()
					webm.href = file_objects[0]["url"] + "?file=webm"
					webm.is_access = "true"
					webm.label = "WebM"
					webm.filename = os.path.splitext(file_objects[0]["name"])[0] + ".webm"
					webm.mime_type = "video/webm"
					dao.file_versions = []
					dao.file_versions.append(original)
					dao.file_versions.append(webm)
				elif ext in original_exts:
					original = FileVersion()
					original.href = file_objects[0]["url"]
					original.is_original = "true"
					original.filename = file_objects[0]["name"]
					original.mime_type = file_objects[0]["mime"]
					if ext == ".pdf":
						original.label = "PDF (original)"
						original.is_access = "true"
					else:
						original.label = "Original"
					dao.file_versions = []
					dao.file_versions.append(original)
				else:
					raise Exception("Unexpected file format for " + dao.uri + " : " + filename)


		for dao in component.digital_objects:

			if quick is True:
				pass
			else:
				exts = []
				for fv in dao.file_versions:
					exts.append(os.path.splitext(fv.filename)[1])
				for priority in self.tika_priorities:
					if priority in exts:
						tika_href = dao.file_versions[exts.index(priority)].href
						tika_cmd = " ".join(["java", "-jar", self.tika_path, "--text", tika_href])
						#print ("running " + tika_cmd)
						tika_content = subprocess.Popen(tika_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
						out, err = tika_content.communicate()
						if tika_content.returncode != 0:
							print (err)
							raise Exception("Unable to access Apache Tika. Is $TIKA_PATH set correctly?")
						dao.content = out.decode(self.tika_encoding)

						break

		return component
