from email.message import EmailMessage
import os
import smtplib
from  python_random_strings.python_random_strings import random_strings 
from multiprocessing import Process


fromEmail = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASSWORD")
    
def send_otp_proccess(toEmail : str,otp : int) :
    em = EmailMessage()

    em['Subject'] = f'Permintaan Reset Password'
    em.set_content(f"Reset Password Dengan OTP {otp}")


    em['From'] = fromEmail

    em['To'] = toEmail
    smtp = smtplib.SMTP('smtp.gmail.com',587)

    smtp.set_debuglevel(False)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(fromEmail,password)
    smtp.sendmail(fromEmail,toEmail,em.as_string())
    
async def sendOtp(toEmail : str) :
    otp = random_strings.random_digits(6)
    p = Process(target=send_otp_proccess,args=(toEmail,otp,))
    p.start()
    return otp