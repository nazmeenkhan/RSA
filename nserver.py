import socket

from Crypto.PublicKey import RSA
from Crypto import Random
from base64 import b64encode, b64decode
import rsa

keysize=1024
random_generator = Random.new().read
key = RSA.generate(keysize, random_generator)
private, public= key, key.publickey()

s = socket.socket()

print ("Socket created")
HOST = '127.0.0.1'  
PORT = 5050
s.bind((HOST,PORT))
s.listen(5) 
conn, address = s.accept()
conn.send(public.exportKey())
conn.send(private.exportKey())
ch = int(conn.recv(1024))
if ch==1:
	while (True):
		try:
			msg=conn.recv(2048)
			decryptor=(rsa.decrypt(b64decode(msg),private)).decode()
			print(decryptor)
			msgc= input('Enter message:').encode()
			if msgc == b'Quit':	
				conn.send(msgc)
				conn.close()
				break
			else:
				encrypted = b64encode(rsa.encrypt(msgc, public))
				conn.send(encrypted)
		except KeyboardInterrupt:
			conn.close()
			break
elif ch==2:
	print('Digital Signature')
	msg = conn.recv(1024)
	sign = conn.recv(1024)
	verify = rsa.verify(msg, b64decode(sign),public)
	print('Is the Sender Verified ?', verify)
	conn.close()
elif ch==3:
	print('Encryption Decryption With Digital Signature')
	msg = conn.recv(2048)
	decryptor=rsa.decrypt(b64decode(msg),private)
	sign = conn.recv(1024)
	verify = rsa.verify(decryptor, b64decode(sign), public)
	print('Is the Sender Verified ?', verify)
	if verify:
		print(decryptor.decode())
	else:
		print('User Is not verified')
		conn.close()
else:
	s.close()				

