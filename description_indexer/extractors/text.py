import os
import requests

class Text():
	"""
	This class extracts text from plain text files using a temp directory
	"""

	def __init__(self):
		pass

	
	def extract(href):

		r = requests.get(href, stream=True)
		#r.raw.decode_content = True
		with open(r.content) as f:
			content = f.read()

			return content
