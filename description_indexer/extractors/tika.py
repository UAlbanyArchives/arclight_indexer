import os
import subprocess

class Tika():
	"""
	This class extracts text from office documents or pdfs using Apache Tika
	requires tika-app.jar file in $TIKA_PATH
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

	
	def extract(self, href):

		tika_cmd = " ".join(["java", "-jar", self.tika_path, "--text", href])

		#print ("running " + tika_cmd)
		tika_content = subprocess.Popen(tika_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = tika_content.communicate()
		if tika_content.returncode != 0:
			print (err)
			raise Exception("Unable to access Apache Tika. Is $TIKA_PATH set correctly?")
		content = out.decode(self.tika_encoding)

		return content