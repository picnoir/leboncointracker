import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(apartments):
    """Notify the use of the apartments given in parameter
       Source of that piece of code: 
       https://stackoverflow.com/questions/10147455/trying-to-send-email-gmail-as-mail-provider-using-python"""
    msg = MIMEMultipart()
    to_addr = ['baylac.felix@gmail.com']
    from_addr = 'GMAILADDR'
    msg['Subject'] = "{} nouvelle offre(s)!".format(len(apartments))
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addr)
    body = ""
    for apartment in apartments:
        body += "\n{}m2, {} pièces dans le {}ème pour {}€. lien: {}".\
            format(apartment.surface, apartment.nb_rooms,
                   apartment.zip_code[-2:], apartment.price, apartment.url)
    msg.attach(MIMEText(body, 'plain'))
    username = from_addr
    password = 'GMAILPASSWORD'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()
