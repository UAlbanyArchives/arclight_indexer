import json
import requests
import subprocess
from os import environ, path
from description_indexer.dao_plugins import DaoSystem

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
		metadata_fields = {"title": "title",
						 "date_uploaded": "date_uploaded",
						 "accession": "accession", 
						 "resource_type": "type", 
						 "processing_activity": "processing_activity",
						 "coverage": "coverage",
						 "extent": "extent",
						 "date_created": "date",
						 "creator": "creator",
						 "contributor": "contributor",
						 "description": "description",
						 "abstract": "abstract",
						 "keyword": "keyword",
						 "subject": "subject",
						 "language": "language"
						 }

		for field in metadata_fields.keys():
			if len(record_json[field]) > 0:
				dao.metadata[metadata_fields[field]] = record_json[field]
		
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


		# requires tika-app.jar file in $TIKA_PATH
		tika_path = "\"" + str(path.join(environ.get("TIKA_PATH"), "tika-app.jar")) + "\""
		print (tika_path)
		print (" ".join(["java", "-jar", tika_path, "--json", dao.href]))
		tika_json = subprocess.Popen(" ".join(["java", "-jar", tika_path, "--json", dao.href]), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = tika_json.communicate()
		print (tika_json.returncode)
		#if len(err) > 0:
		#	print (err)
		#	raise Exception("Unable to access Apache Tika. Is $TIKA_PATH set correctly?")
		tika_metadata = json.load(out.decode('utf8'))
		for key in tika_metadata.keys():
			print ("\n" + key)


		#filename = fields.StringField()
		#mime_type = fields.StringField()

		return dao