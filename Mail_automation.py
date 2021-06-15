import smtplib, ssl

class Mail():
    def __init__(self, database, message, passphrase, encryption_protocol="SSL"):
        self.DB = database
        self.sender = "Insert_sender's_mail-address_here"
        self.receiver = "Insert_receiver's_mail-address_here"
        self.host = "smtp.gmail.com"
        self.username = self.sender
        self.passphrase = passphrase

        context = ssl.create_default_context()

        if encryption_protocol == "TSL":
            self.port = 587
            server = smtplib.SMTP(self.host, self.port)
            server.starttls(context=context)  # Secure the connection
            server.login(self.username, self.passphrase)
            server.sendmail(self.sender, self.receiver, message)

        elif encryption_protocol == "SSL":
            self.port = 465
            with smtplib.SMTP_SSL(self.host, self.port, context=context) as server:
                server.login(self.username, self.passphrase)
                server.sendmail(self.sender, self.receiver, message)

        else:
            raise ("Invalid Encryption protocol.\n Please select either \"TLS\" or \"SSL\"")

