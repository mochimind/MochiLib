import socket

HOST = "localhost"
PORT = 19331
MAX_LEN_BITS = 4


def sendMessage(sock, data):
	data = data.encode('utf-8')
	total_sent = 0
	len_str = str(len(data))
	if len(len_str) < MAX_LEN_BITS:
		len_str = len_str.rjust(MAX_LEN_BITS, "0").encode("utf-8")
	try:
		while total_sent < MAX_LEN_BITS:
			sent = sock.send(len_str[total_sent:])
			if sent == 0:
				print("error: socket connection broken")
				return False
			total_sent += sent

		total_sent = 0
		while total_sent < len(data):
			sent = sock.send(data[total_sent:])
			if sent == 0:
				print("error: socket connection broken")
				return False
			total_sent += sent
	except socket.error as e:
		print("terminated by client " + e.message)
		return False

	return True

def readPacket(sock):
	# first get the size of the message
	size_bytes = readBytes(sock, MAX_LEN_BITS)
	if size_bytes is None:
		return None

	try:
		data = readBytes(sock, int(size_bytes))
		return data.strip()
	except ValueError:
		print("error: received non-valid length segment: " + size_bytes)
		return None

def readBytes(sock, n):
	data = b''
	try:
		while len(data) < n:
			packet = sock.recv(n - len(data))
			if not packet:
				return None
			data += packet
	except socket.error as e:
		print("connection terminated by client " + e.message)
		return False

	return data.decode("utf-8")

clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsock.connect(("localhost", 19331))

sendMessage(clientsock, "hello world")
print (readPacket(clientsock))

sendMessage(clientsock, "query")
print (readPacket(clientsock))

sendMessage(clientsock, "query {}")
print (readPacket(clientsock))

sendMessage(clientsock, "query {'input': 'this is a test string'}")
print (readPacket(clientsock))

sendMessage(clientsock, "query {\"input\": \"this is a test string\"}")
print (readPacket(clientsock))

sendMessage(clientsock, "query {\"input\": \"this is a test string\", \"result\": \"data\"}")
print (readPacket(clientsock))

sendMessage(clientsock, "query {\"input\": \"this is a test string\", \"insert\": false}")
print (readPacket(clientsock))

sendMessage(clientsock, "exit")
print (readPacket(clientsock))


