import os
import json
import shutil
import requests
import mimetypes
import subprocess
from description_indexer.dao_plugins import DaoSystem
from description_indexer.models.description import DigitalObject, File, FileVersion

from description_indexer.extractors.tika import Tika
from description_indexer.extractors.text import Text
from description_indexer.extractors.ocr import Ocr

from urllib.request import urlopen
import cgi

class Hyrax(DaoSystem):
	dao_system_name = "hyrax"


	def __init__(self):
		print (f"Setup {self.dao_system_name} dao system for reading digital object data.")

		# initalize extractors
		# Requirements for each need to be installed to initalize
		self.tika = Tika()
		self.text = Text()
		#self.ocr = Ocr()


	def get_mime_type(self, filename):

		# this is easier than getting magic to work crossplatform atm
		docmimes = {
			".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
			".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
			".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
			".odt": "application/vnd.oasis.opendocument.text",
			".rtf": "application/rtf"
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
			for file in dao.files:
				for fv in file.versions:
					fv_count += 1
			if fv_count == 1:
				dao.uri = dao.files[0].versions[0].href.strip()
				# clear file added with ASpace data, we'll add the correct file(s) later
				dao.files = []
			else:
				raise Exception ("ASpace DAO unexpectedly has multiple file versions! --> " + str(dao.uri))			

			dao.metadata = {}
			#print ("reading " + dao.uri + "?format=json")
			if dao.uri.startswith("https://archives.albany.edu/catalog?f%5Barchivesspace_record_tesim"):
				#record_json = requests.get(dao.uri + "?format=json").json()
				continue
			elif dao.uri.startswith("https://web.archive.org/web"):
				#record_json = requests.get(dao.uri + "?format=json").json()
				continue
			elif dao.uri.startswith("https://wayback.archive-it.org"):
				continue
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
			# some jsondl graphs have duplicate files for some reason
			dupIDs = []
			# some daos don't have @graph keys?
			if not "@graph" in jsonld.keys():
				if not "ebucore:hasRelatedMediaFragment" in jsonld.keys():
					#print (jsonld)
					raise Exception("Missing keys in JSONLD?")
				else:
					fileSetID = jsonld["ebucore:hasRelatedMediaFragment"]["@id"].split("archives.albany.edu/catalog/")[1]
					dupIDs.append(fileSetID)
			else:
				for fileObject in jsonld["@graph"]:
					if "ore:proxyFor" in fileObject.keys():
						fileSetID = fileObject["ore:proxyFor"]["@id"].split("archives.albany.edu/catalog/")[1]
						if not fileSetID in dupIDs:
							dupIDs.append(fileSetID)
			for fileSetID in set(dupIDs):
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

			rights = dao.rights_statement
			metadata = dao.metadata
			subjects = dao.subjects
			dao_id = dao.identifier
			dao_uri = dao.uri

			manual_versions = False
			manual_version_exceptions = ["8910kc626", "9019sk86q", "0c484314x", "d217r7481"]
			if "/daos/" in dao.uri and dao.uri.split("/daos/")[1] in manual_version_exceptions:
				manual_versions = True

			if len(file_objects) == 1 or manual_versions:
				# digital object with a single file
				# or manual_versions with multiple files that are really versions

				# single item was uploaded to hyrax, but converted into derivatives
				# single digital objects that may have multiple versions
				#original_exts = [".pdf", ".csv"]
				office_docs = [".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt"]
				audio_exts = [".mp3"]
				video_exts = [".mpg", ".mp4", ".mov", ".avi"]

				if manual_versions == False and len(set(extentions)) > 1:
					raise Exception("Unexpectedly discovered multiple file extentions for " + dao.url)
				else:
					ext = extentions[0]

				if len(set(mimes)) == 1 and mimes[0].lower().startswith("image"):
					# for images use iiif
					dao.iiif_manifest = dao_uri + "/manifest"

				file = File()
				file.identifier = file_objects[0]["url"].split("?")[0].split("/downloads/")[1]
				file.thumbnail_href = file_objects[0]["url"] + "?file=thumbnail"
				if manual_versions:
					for fo in file_objects:
						mv = FileVersion()
						mv.href = fo['url']
						mv.filename = fo['name']
						mv.mime_type = fo['mime']
						if fo['ext'].lower() == ".pdf":
							mv.label = "PDF (Original)"
							mv.is_original = "true"
							mv.is_access = "true"
						elif fo['ext'].lower() == ".csv":
							mv.label = "CSV data"
						elif fo['ext'].lower() == ".xlsx":
							mv.label = "Spreadsheet"
						file.versions.append(mv)
				elif ext in office_docs:
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
					file.versions.append(original)
					file.versions.append(pdf)
				elif ext in audio_exts:
					mp3 = FileVersion()
					mp3.href = file_objects[0]["url"] + "?file=mp3"
					mp3.label = "MP3"
					mp3.is_original = "true"
					mp3.filename = file_objects[0]["name"]
					mp3.mime_type = file_objects[0]["mime"]
					ogg = FileVersion()
					ogg.href = file_objects[0]["url"] + "?file=ogg"
					ogg.is_access = "true"
					ogg.label = "Ogg"
					ogg.filename = os.path.splitext(file_objects[0]["name"])[0] + ".ogg"
					ogg.mime_type = "audio/ogg"
					file.versions.append(mp3)
					file.versions.append(ogg)
				elif ext in video_exts:
					original = FileVersion()
					original.href = file_objects[0]["url"]
					original.label = "Original"
					original.is_original = "true"
					original.filename = file_objects[0]["name"]
					original.mime_type = file_objects[0]["mime"]
					webm = FileVersion()
					webm.href = file_objects[0]["url"] + "?file=webm"
					webm.is_access = "true"
					webm.label = "WebM"
					webm.filename = os.path.splitext(file_objects[0]["name"])[0] + ".webm"
					webm.mime_type = "video/webm"
					file.versions.append(original)
					file.versions.append(webm)
				else:
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
					
					file.versions.append(original)
				
				# append file to dao
				dao.files.append(file)


			else:
				# these are really Components or aggregages of DOs currently managed in Hyrax
				# example: daos/wp988s44h or daos/j9602614q
				# exceptions: daos/8910kc626

				component.digital_objects = []
				if len(set(mimes)) == 1 and mimes[0].lower().startswith("image"):
					# for images use iiif
					component.iiif_manifest = dao_uri + "/manifest"

				fo_count = 0
				representativeness = "false"
				for file_object in file_objects:
					fo_count += 1
					do = DigitalObject()
					do.uri = f"https://archives.albany.edu/concern/parent/{dao_uri.rsplit('/', 1)[1]}/file_sets/{file_object['url'].split('/downloads/')[1]}"
					do.label = file_object["name"]
					do.identifier = dao_id + "-" + str(fo_count)
					do.is_representative = representativeness
					do.thumbnail_href = file_object["url"] + "?file=thumbnail"
					do.rights_statement = rights
					do.metadata = metadata
					do.subjects = subjects

					file = File()
					file.identifier = file_object["url"].split("?")[0].split("/downloads/")[1]
					file.thumbnail_href = file_object["url"] + "?file=thumbnail"
					fv = FileVersion()
					fv.href = file_object["url"]
					fv.is_access = "true"
					fv.is_original = "true"
					fv.filename = file_object["name"]
					fv.mime_type = file_object["mime"]
					file.versions.append(fv)
					do.files.append(file)
					component.digital_objects.append(do)

		#######################################

		# Extract content for better discovery

		# for versions, this is a priortized list of exts to pull content from
		priorities = (".txt", ".csv", ".docx", ".pptx", ".xlsx", ".doc", ".ppt", ".xls", ".pdf", ".jpg", ".png", ".tif", ".wav", ".mp3", ".ogg", ".mpg", ".mp4", ".mov", ".avi", ".webm")

		read_file = (".txt", ".csv", ".rtf")
		tika_exts = (".docx", ".pptx", ".xlsx", ".doc", ".ppt", ".xls", ".pdf", ".jpg", ".png", ".tif")
		# Might break out OCR in the future to try something like PaddleOCR (https://github.com/PaddlePaddle/PaddleOCR) rather than Tesseract
		#tika_ocr = (".pdf")
		#ocr = (".jpg", ".png", ".tif")
		audio = (".wav", ".mp3", ".ogg")
		video = (".mpg", ".mp4", ".mov", ".avi", ".webm")
		

		for dao in component.digital_objects:

			if quick is True:
				pass
			else:
				cache_path = os.path.join(os.path.expanduser("~"), ".description_indexer", dao.identifier)

				for file in dao.files:
					cache_file = os.path.join(cache_path, file.identifier + ".txt")
					content = ""

					if os.path.isfile(cache_file):
						with open(cache_file, "r") as cache:
							content = cache.read()
					else:

						# Gather a list of all extentions in versions
						exts = []
						for fv in file.versions:
							exts.append(os.path.splitext(fv.filename)[1].lower())

						for priority in priorities:
							# Get the first match in priorities set
							if priority in exts:
								extract_file = file.versions[exts.index(priority)]

								if priority in read_file:
									content = self.text.extract(extract_file.href)

								elif priority in tika_exts:
									content = self.tika.extract(extract_file.href)

								if len(content.strip()) > 0:
									# write to disk to speed reindexing
									if not os.path.isdir(cache_path):
										os.makedirs(cache_path)
									with open(cache_file, "w") as cache:
										cache.write(content)

								break

					file.content = content


		return component
