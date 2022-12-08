import chardet
import requests

class Text():
	"""
	This class extracts text from plain text files using a temp directory
	"""

	def __init__(self):
		pass

	
	def extract(self, href):

		content = ""

		r = requests.get(href, stream=True)
		#r.raw.decode_content = True
		if r.status_code == 200:
			try:
				# try utf-8 first
				content = r.content.decode("utf-8")
			except:
				try:
					# try windows encoding
					content = r.content.decode("cp1252")
				except:
					try:
						# try to detect
						encoding = chardet.detect(r.content)["encoding"]
						content = r.content.decode(encoding)
					except:
						print ("Unable to decode file.")


		return content
