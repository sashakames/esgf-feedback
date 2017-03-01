from email.mime.text import MIMEText
import smtplib
from threading import Thread

class EmailConfig:
    '''
    Class that stores the email server connection properties from a local configuration file.
    Site specific values are read from the cog_settings.cfg file through the SiteManager class.
    '''
    def __init__(self):
        self.init = False
        self.server = "nospam.llnl.gov"

        self.sender = "ames4@llnl.gov"  # Testing purposes - change based on properties
        print 'Using email sender=%s' %  self.sender
        self.init = True
            
        if not self.init:
            print "Email configuration not found, email notification disabled"
            
# module scope email configuration
emailConfig = EmailConfig()

def notify(toUser, subject, message, mime_type='plain'):  # send 'plain' email by default
    
    # send email in separate thread, do not wait   
    emailThread = EmailThread(toUser.email, subject, message, mime_type=mime_type)
    emailThread.start()

def sendEmail(fromAddress, toAddress, subject, message):
    
    # send email in separate thread, do not wait
    emailThread = EmailThread(toAddress, subject, message, fromAddress=fromAddress)
    emailThread.start()

        
class EmailThread(Thread):
    '''Class that sends an email in a separate thread.'''
    
    def __init__ (self, toAddress, subject, message, fromAddress=None, mime_type='plain'):
        Thread.__init__(self)
        self.toAddress = toAddress
        self.subject = subject
        self.message = message
        if fromAddress is not None:
            self.fromAddress = fromAddress
        elif emailConfig.init == True:
            self.fromAddress = emailConfig.sender
        else:
            self.fromAddress = None
        self.mime_type=mime_type
        
    def run(self):
        
        #print "From: %s" % self.fromAddress
        print "To: %s" % self.toAddress
        print "Subject: %s" % self.subject
        print "Message: %s" % self.message
        print "Mime Type: %s" % self.mime_type
        
        # use local mail server
        #toUser.email_user(subject, message, from_email=fromAddress)
        
        # use email relay server
        if emailConfig.init == True:
    
            # use email relay server
            msg = MIMEText(self.message, self.mime_type)
            msg['Subject'] = self.subject
            msg['From'] = self.fromAddress
            msg['To'] = self.toAddress    
            if emailConfig.port is not None:
                s = smtplib.SMTP(emailConfig.server, emailConfig.port)
            else:
                s = smtplib.SMTP(emailConfig.server)
            if emailConfig.security=='STARTTLS':
                s.starttls()
            if emailConfig.username and emailConfig.password:
                s.login(emailConfig.username, emailConfig.password )
            s.sendmail(emailConfig.sender, [self.toAddress], msg.as_string())
            s.quit()
            print 'Email sent.'
