import smtplib

sender = "william.ahrons@gmail.com"
receiver = ["william.ahrons@gmail.com"]
message = "Hello!"

try:    
    session = smtplib.SMTP('smtp.gmail.com',587)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(sender,'06baskete')
    session.sendmail(sender,receiver,message)
    session.quit()

except smtplib.SMTPException as e:
    print(e)
