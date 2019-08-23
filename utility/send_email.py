import requests


def send(name, email, subject, text):
	"""

	:param name: the name of the recipient
	:param email: email address of the recipient
	:param subject: email subject
	:param text: email content
	:return:
	"""
	return requests.post(
		"https://api.mailgun.net/v3/sandbox196dde48970e40598a832b82fd5f8430.mailgun.org/messages",
		auth=("api", "98fc3bf073110ec99e95cb3bf3e54961-2ae2c6f3-9f77f352"),
		data={
			"from": "Wall Master <master@wall.com>",
			"to": "%s <%s>" % (name, email),
			"subject": subject,
			"text": text
		}
	)
