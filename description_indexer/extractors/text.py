import os
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
			content = r.content.decode()	

		return content
