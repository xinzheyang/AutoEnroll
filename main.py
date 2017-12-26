import getpass
import parse
import enroll
import json
import smtplib
from email.mime.text import MIMEText

def send(email, passwd, target, receiver):
	server = smtplib.SMTP("smtp.gmail.com", 587)

	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(email, passwd)

	msg = MIMEText("Congrats!") # The /n separates the message from the headers (which we ignore for this ex
	msg["Subject"] = "A new spot for %s" %target
	for person in receiver:
		server.sendmail(email, person, msg.as_string())

class Bot:

	def __init__(self):
		"""
		target = raw_input("Please enter the class you want to add, case and space sensitive. eg. 'CS 3110 DIS 202':")
		email = raw_input("Please enter the Gmail address you want to send and receive notifications: ")
		email_pass = getpass.getpass("Please enter the email passward: ")
		netID = raw_input("Please enter your Cornell NetID: ")
		netID_pass = getpass.getpass("Please enter your Cornell NetID passward: ")
		"""
		config = json.loads(open("credentials.json").read())
		print config
		self.driver = None
		self.target = config["target"]
		self.prefer = config["prefer"]
		self.email = config["email"]
		self.email_pass = config["email_pass"]
		self.receiver = config["receiver"]
		self.netID = config["netID"]
		self.netID_pass = config["netID_pass"]

	def main(self):
		while True:
			section = parse.get_section(self.target)
			status = parse.is_open(section)
			print status
			if status:
				send(self.email, self.email_pass, self.target, self.receiver)
				number = parse.get_five_digit(section)
				self.driver = enroll.init()
				enroll.preadd(self.driver, self.netID, self.netID_pass)
				enroll.add(self.driver, number, self.prefer)
				break
def run():
	while True:
		try:
			b = Bot()
			b.main()
		
		except:
			b.driver.quit()
			continue
			
if __name__ == '__main__':
	run()

