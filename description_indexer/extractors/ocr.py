import os
import cgi
import shutil
import tempfile
from urllib.request import urlopen
from urllib.request import urlretrieve

class Ocr():
	"""
	This class extracts text from images with OCR
	requires pdf2image (https://github.com/Belval/pdf2image) which requires Poppler library
	which needs to be installed on Windows (https://blog.alivate.com.au/poppler-windows/)
	"""

	def __init__(self):
		pass

	
	def extract(self, href):

		#tempdir = tempfile.mkdtemp()

		"""
		remotefile = urlopen(href)
		content_disposition = remotefile.info()['Content-Disposition']
		filename = cgi.parse_header(content_disposition)[1]["filename"]

		urllib.request.urlretrieve(href, os.path.join(tempdir, filename))

		if filename.lower().endswith(".pdf"):
		"""



		content = ""

		#shutil.rmtree(tempdir)

		return content