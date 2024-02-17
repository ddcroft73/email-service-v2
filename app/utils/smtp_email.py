from smtplib import SMTP_SSL, SMTPException
from ssl import create_default_context
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config.settings import settings
from app.api.schema.schema import Email, TextMessage
from typing import Any

from .logger import logzz

# Simple Class for sending smtp emails. THe class is instantioed after definiton with all the 
# necessary data to connect to an email account and send mail.

#  Send mail async, send mail using celery (There is a lot more to that than n the class)
#  send text message through email. THis requires the provider of the cell service being sent to;


class SmtpEmail():
    def __init__(self, smtp_host: str, smtp_port: int, username: str, password: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def prepare_message(
        self, em_from: str, em_to: str, sub: str, html: str, text: str=None
    ) -> str:
        message = MIMEMultipart("alternative")
        message["Subject"] = sub
        message["From"] = em_from
        message["To"] = em_to

        txt_part = MIMEText(text, "plain")
        html_part = MIMEText(html, "html")

        message.attach(txt_part)
        if not html == "":
            message.attach(html_part)

        return message.as_string()

    def send_mail(self, email: Email) -> bool:

        _message = self.prepare_message(
            email.email_from, email.email_to, email.subject, email.message, ''
        )
                
        try:
           with SMTP_SSL(self.smtp_host, self.smtp_port, context=create_default_context()) as email_:
             email_.login(self.username, self.password)
             email_.sendmail(self.username, email.email_to, _message)
             
             logzz.info("Email sent via email your email 'Provider' ", timestamp=True)
             return True 
             
        except SMTPException as smtp_err:
            logzz.error('SMTP Error:', smtp_err)
            return False    
        
        except Exception as er:
           logzz.error('Exception occured sending mail:', smtp_err)
           return False               

       
        
    async def send_async(self, email: Email) -> bool:
        
        _message = self.prepare_message(
            email.email_from, email.email_to, email.subject, email.message, ''
        )
        #sleep(random.randint(5, 15))
        
        try:
           with SMTP_SSL(self.smtp_host, self.smtp_port, context=create_default_context()) as email_:
             email_.login(self.username, self.password)
             email_.sendmail(self.username, email.email_to, _message)

             logzz.info(
                f"Email sent via your email 'Provider' to: {email.email_to} ", 
                timestamp=True
             )
             return True
             
        except SMTPException as smtp_err:
            logzz.error(f" SMTP ERROR: {smtp_err}")
            return False    
        
        except Exception as er:
           logzz.error(f"Exception occurred attepmting to send mail. \n{str(er)}")
           return False                  
        
    

    async def send_text_message(self, text_message: TextMessage) -> bool:
        '''
           Sends a text message to cell number using email
        '''
        try:
           with SMTP_SSL(self.smtp_host, self.smtp_port, context=create_default_context()) as email:
             email.login(self.username, self.password)
             email.sendmail(self.username, text_message.text_to, text_message.message)

             return True
             
        except SMTPException as smtp_err:
            logzz.error(f" SMTP ERROR: {smtp_err}")
            return False    
        
        except Exception as er:
           logzz.error(f"Exception occurred attepmting to send a TEXT. \n{str(er)}")
           return False               
        

        
    


# Instantiate as Singleton... technically
smtp_email = SmtpEmail(
    settings.SMTP_SERVER,
    settings.SMTP_PORT,
    settings.EMAIL_LOGIN,
    settings.EMAIL_PASSWRD,
)
