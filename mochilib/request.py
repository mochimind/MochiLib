import socket
import threading

from . import command

MAX_LEN_BITS = 4
ERROR_RESPONSE = "Error"
OK_RESPONSE = "OK"

EXIT_COMMAND = "exit"
ANALYZE_COMMAND = "analyze"
QUERY_COMMAND = "query"

class RequestProcessor (threading.Thread):
	def __init__(self, sock):
		self.socket = sock

	def run(self):
		while True:
			data = self.readPacket()
			print("got: ", data)

			if data is None:
				self.handleError("error: could not read data from socket", True, False)
				return

			comm = command.GetCommand(data)
			if not comm.valid:
				self.handleError(comm.error_str, False, True)
				continue

			if type(comm) is command.ExitCommand:
				self.handleError("client closed", True, False)
				return
			else:
				comm.execute()
				#self.sendMessage(OK_RESPONSE if analysis.handleAnalyze() else ERROR_RESPONSE + analysis.getResultString() + "\n")

	def readPacket(self):
		# first get the size of the message
		size_bytes = self.readBytes(MAX_LEN_BITS)
		if size_bytes is None:
			return None

		try:
			data = self.readBytes(int(size_bytes))
			return data.strip()
		except ValueError:
			print("error: received non-valid length segment: " + size_bytes)
			return None

	def readBytes(self, n):
		data = b''
		try:
			while len(data) < n:
				packet = self.socket.recv(n - len(data))
				if not packet:
					return None
				data += packet
		except socket.error as e:
			print("connection terminated by client " + e.message)
			return False

		return data.decode("utf-8")

	def handleError(self, msg, terminal, send_response):
		print (msg)
		if send_response:
			self.sendMessage(ERROR_RESPONSE + " " + msg + "\n")
		if terminal:
			self.socket.close()

	def sendMessage(self, data):
		data = data.encode('utf-8')
		total_sent = 0
		len_str = str(len(data))
		if len(len_str) < MAX_LEN_BITS:
			len_str = len_str.rjust(MAX_LEN_BITS, "0").encode("utf-8")
		try:
			while total_sent < MAX_LEN_BITS:
				sent = self.socket.send(len_str[total_sent:])
				if sent == 0:
					print("error: socket connection broken")
					return False
				total_sent += sent

			total_sent = 0
			while total_sent < len(data):
				sent = self.socket.send(data[total_sent:])
				if sent == 0:
					print("error: socket connection broken")
					return False
				total_sent += sent
		except socket.error as e:
			print("terminated by client " + e.message)
			return False

		return True

	def __repr__(self):
		return "RequestProcessor"

