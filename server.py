from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
from os import curdir, sep
import os
import code_testing

ADDR = "0.0.0.0"
PORT = 80

class RequestHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		length = int(self.headers['Content-length'])
		content = self.rfile.read(length)
		content = parse_qs(content)

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
			result = code_testing.submitTestCode(self.path, code_proposition)

			htmlContent = htmlContent.replace("<!--OUT--->", result)

			self.wfile.write(htmlContent)
			f.close()
		except:
			self.wfile.write("Fail creating subprocess")


	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"

		sendReply = False
		if self.path.endswith(".html"):
			mimetype='text/html'
			sendReply = True
		if self.path.endswith(".jpg"):
			mimetype='image/jpg'
			sendReply = True
		if self.path.endswith(".gif"):
			mimetype='image/gif'
			sendReply = True
		if self.path.endswith(".js"):
			mimetype='application/javascript'
			sendReply = True
		if self.path.endswith(".css"):
			mimetype='text/css'
			sendReply = True

		if sendReply == True:
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
