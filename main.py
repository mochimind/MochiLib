
import socket
from mochilib import command
from mochilib import request


HOST = "localhost"  # use "" for all network
PORT = 19331
CONNECTIONS = 5

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.bind((HOST, PORT))
serversock.listen(CONNECTIONS)


while 1:
    (clientsock, addr) = serversock.accept()
    processor = request.RequestProcessor(clientsock)
    processor.run()

