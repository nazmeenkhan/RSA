import socket
from Crypto.PublicKey import RSA
from Crypto import Random
from base64 import b64decode , b64encode 
import rsa

keysize=1024
random_generator = Random.new().read
key = RSA.generate(keysize, random_generator)
private1, public1= key, key.publickey()

c=socket.socket()
HOST= '127.0.0.1'
PORT = 5050
c.connect((HOST, PORT))
  
public=rsa.importKey(c.recv(2048))
private = rsa.importKey(c.recv(2048))
print("1-encryption\n2-digital signature\n3-both\n4-quit")

ch=input("enter your choice").encode()
c.send(ch)
if int(ch) == 1:

	while True:
		try:
			msg = input('Enter message:').encode()
			encrypted = b64encode(rsa.encrypt(msg,public))
			c.send(encrypted)
			msgc=c.recv(2048)
			if msgc.decode() == 'Quit':
				c.close()
				break
			else:
				print(rsa.decrypt(b64decode(msgc), private).decode())
		except KeyboardInterrupt:
			c.close()
			break
elif int(ch)==2:

	msg = input('Enter Message:').encode()
	c.send(msg)
	signature = b64encode(rsa.sign(msg, private))
	c.send(signature)
elif int(ch)==3:

	print('Encryption Decryption With Digital Signature')
	msg = input('Enter Message:').encode()
	encrypted = b64encode(rsa.encrypt(msg,public))
	c.send(encrypted)
	signature = b64encode(rsa.sign(msg, private))
	c.send(signature)
else:
	exit()