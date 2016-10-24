from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
from os import curdir, sep
import os
from code_testing import CodeTester
import re


exerciceUrl = re.compile("^[0-9]+$")
resultUrl = re.compile("^r[0-9]+$")

ADDR = "0.0.0.0"
PORT = 80

codeTester = CodeTester()
exerciceList = []

for file in os.listdir("exercices"):
	if file.endswith(".ex"):
		with open("exercices/" + file, 'r') as f:
			data = f.read().split('###&###')

		test = data[7].split("#&#")
		# Remove linebreak
		for j in range(len(test)):
			test[j] = test[j][1:]
			test[j] = test[j][:-1]

		# Create exercice
		exerciceList.append({
					"subject" : data[0],
					"description" : data[1],
					"difficulty" : data[2],
					"statement" : data[3],
					"extra" : data[4],
					"before code" : data[5],
					"import" : data[6],
					"tests" : test
							})

class RequestHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		length = int(self.headers['Content-length'])
		content = self.rfile.read(length)
		content = parse_qs(content)
		exercice_id = int(self.path[2:])

		# Send the code proposition
		code_proposition = content['proposed_code'][0]

		try:
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
		except:
			self.send_response(200)
			self.end_headers()
			self.wfile.write("Fail creating page")

		try:
			f = open(curdir + sep + 'result.html')

			htmlContent = f.read()
			# before_code, test_code, submited_code
			result = codeTester.submitTestCode(exerciceList[exercice_id]["import"], exerciceList[exercice_id]["tests"], code_proposition)

			htmlContent = htmlContent.replace("<!--OUT--->", result)
			htmlContent = htmlContent.replace("<!--SUBJECT--->", exerciceList[exercice_id]["subject"])

			self.wfile.write(htmlContent)
			f.close()
		except:
			self.wfile.write("Fail creating subprocess")


	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"

		# Content type
		if self.path.endswith(".html"):
			mimetype='text/html'
		if self.path.endswith(".jpg"):
			mimetype='image/jpg'
		if self.path.endswith(".gif"):
			mimetype='image/gif'
		if self.path.endswith(".js"):
			mimetype='application/javascript'
		if self.path.endswith(".css"):
			mimetype='text/css'

		# Exercice selection
		if self.path == "/index.html":
			f = open(curdir + sep + self.path)
			self.send_response(200)
			self.send_header('Content-type',mimetype)
			self.end_headers()

			htmlContent = f.read()
			f.close()
			with open('exercices/description.des', 'r') as des:
				data = des.read().replace('\n', '</br>')

			htmlContent = htmlContent.replace("<!--DESCRIPTION--->", data)

			exerciceContent = ""
			for e in range(len(exerciceList)):
				d = exerciceList[e]["difficulty"].replace('\n', '')
				exerciceContent += "<div class=\"panel panel-default\"> \
				<div class=\"panel-body\"> \
					<h4>" + exerciceList[e]["subject"] + "</h4> \
					<p>Sample description</p> \
					<div class=\"progress\"> \
						<div class=\"progress-bar progress-bar-striped\" \
						role=\"progressbar\" aria-valuenow=" + d + " aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width:" + d + "%;\"> \
							<span class=\"sr-only\">Difficulty</span> \
						</div> \
					</div> \
					<a href=" + str(e) + "><button type=\"button\" class=\"btn btn-primary\">Solve</button></a> \
				</div> \
			</div>"

			htmlContent = htmlContent.replace("<!--EXERCICES--->", exerciceContent)

			self.wfile.write(htmlContent)
		elif exerciceUrl.match(self.path[1:]) is not None:
			i = int(self.path[1:])

			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()

			f = open(curdir + sep + "/exercice.html")
			htmlContent = f.read()

			# Add content
			htmlContent = htmlContent.replace("<!--SUBJECT--->", exerciceList[i]["subject"])
			htmlContent = htmlContent.replace("<!--STATEMENT--->", exerciceList[i]["statement"])
			htmlContent = htmlContent.replace("<!--EXTRA--->", exerciceList[i]["extra"])
			htmlContent = htmlContent.replace("<!--BEFORE CODE--->", exerciceList[i]["before code"])
			htmlContent = htmlContent.replace("<!--EXERCICE ID--->", str(i))

			self.wfile.write(htmlContent)
			f.close()

		else:
			#Open the static file requested and send it
			f = open(curdir + sep + self.path)
			self.send_response(200)
			self.send_header('Content-type',mimetype)
			self.end_headers()
			self.wfile.write(f.read())
			f.close()
		return

httpd = HTTPServer((ADDR, PORT), RequestHandler)
httpd.serve_forever()
