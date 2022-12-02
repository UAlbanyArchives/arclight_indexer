import os
import subprocess

class Tika():
	"""
	This class extracts text from office documents or pdfs using Apache Tika
	requires tika-app.jar file in $TIKA_PATH
	For OCR to work tesseract is also required
	To OCR PDFs, you also need a tika-config.xml file in $TIKA_PATH per
	https://stackoverflow.com/questions/51655510/how-do-you-enable-the-tesseractocrparser-using-tikaconfig-and-the-tika-command-l#answer-60404894
	"""

	def __init__(self):

		check_java = subprocess.Popen(["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = check_java.communicate()
		if check_java.returncode != 0:
			raise Exception("Unable to access Java")

		if os.name == "nt":
			# tika uses native encoding grrr
			self.tika_encoding = "Windows-1252"
		else:
			self.tika_encoding = "utf-8"
		self.tika_path = "\"" + str(os.path.join(os.environ.get("TIKA_PATH"), "tika-app.jar")) + "\""
		self.tika_config = "\"" + str(os.path.join(os.environ.get("TIKA_PATH"), "tika-config.xml")) + "\""

	
	def extract(self, href):

		if os.path.isfile(self.tika_config):
			tika_cmd = " ".join(["java", "-jar", self.tika_path, f"--config={self.tika_config}", "--text", href])
		else:
			tika_cmd = " ".join(["java", "-jar", self.tika_path, "--text", href])

		#print ("running " + tika_cmd)
		tika_content = subprocess.Popen(tika_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = tika_content.communicate()
		if tika_content.returncode != 0:
			print (err)
			raise Exception("Unable to access Apache Tika. Is $TIKA_PATH set correctly?")
		content = out.decode(self.tika_encoding)

		return content