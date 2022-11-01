import os
import json
import shutil
import requests
import mimetypes
import subprocess
from description_indexer.dao_plugins import DaoSystem

from urllib.request import urlopen
import cgi

class Hyrax(DaoSystem):
	dao_system_name = "hyrax"

	def __init__(self):
		print (f"Setup {self.dao_system_name} dao system for reading digital object data.")

		check_java = subprocess.Popen(["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = check_version.communicate()
		if len(err) > 0:
			raise Exception("Unable to access Java")

	def read_data(dao):
		print ("reading data from " + dao.href + "?format=json")

		dao.metadata = {}

		record_json = requests.get(dao.href + "?format=json").json()

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

		jsonld = requests.get(dao.href + "?format=jsonld").json()
		for fileObject in jsonld["@graph"]:
			if "ore:proxyFor" in fileObject.keys():
				fileSetID = fileObject["ore:proxyFor"]["@id"].split("archives.albany.edu/catalog/")[1]
				fileURL = "https://archives.albany.edu/downloads/" + fileSetID
				dao.href = fileURL
				dao.thumbnail_href = fileURL + "?file=thumbnail"

		# Gotta get the filename from Content-Disposition for mimetype
		remotefile = urlopen(dao.href)
		content_data = remotefile.info()['Content-Disposition']
		value, params = cgi.parse_header(content_data)
		filename = params["filename"]

		mimetype = mimetypes.MimeTypes().guess_type(filename)[0]
		dao.mime_type = mimetype
		dao.metadata["filename"] = filename

		# requires tika-app.jar file in $TIKA_PATH
		if os.name == "nt":
			# tika uses native encoding grrr
			tika_encoding = "Windows-1252"
		else:
			tika_encoding = "utf-8"
		tika_path = "\"" + str(os.path.join(os.environ.get("TIKA_PATH"), "tika-app.jar")) + "\""
		tika_cmd = " ".join(["java", "-jar", tika_path, "--text", dao.href])

		tika_content = subprocess.Popen(tika_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = tika_content.communicate()
		if tika_content.returncode != 0:
			print (err)
			raise Exception("Unable to access Apache Tika. Is $TIKA_PATH set correctly?")
		dao.content = out.decode(tika_encoding)

		return dao
