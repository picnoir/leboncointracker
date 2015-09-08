import smtplib

def send_mail(apartments):
    """Notify the use of the apartments given in parameter
       Source of that piece of code: 
       https://stackoverflow.com/questions/10147455/trying-to-send-email-gmail-as-mail-provider-using-python"""
    fromaddr = 'baylac.felix@gmail.com'
    toaddrs = ['baylac.felix@gmail.com']
    msg = "{} nouvelle offre(s)!".format(len(apartments))
    for apartment in apartments:
        msg += "\n{}m2, {} pièces dans le {}ème pour {}€. lien: {}".\
            format(apartment.surface, apartment.nb_rooms,
                   apartment.zip_code[-2:], apartment.price, apartment.url)
    username = 'yourgmailUsername@gmail.com'
    password = 'yourGmailPassword'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg.encode('utf-8'))
    server.quit()
