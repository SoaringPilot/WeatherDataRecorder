import smtplib
import ssl

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "timothy.clark.dev@gmail.com"
receiver_email = "timothy.clark.dev@gmail.com"
password = "dev_python_88"
message = "Subject: Hi Again\n\nThis is my test message."
# message = """\
# Subject: Hi there
#
# This message is sent from Python."""

# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
try:
    server = smtplib.SMTP(smtp_server,port)
    server.ehlo() # Can be omitted
    server.starttls(context=context) # Secure the connection
    server.ehlo() # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit()