import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

messages = [
    ("""Bonjour Demoiselle Poupoule,

Moi, Arnold le premier, viens de dénicher les offres suvantes sur le bon coin.\n""",
     """Veuillez agréer mes papoulles les plus distinguées

Cordialement,
Arnold le Grand"""),
    ("""Wesh la meuf, ça roule?
Ton nonold il t'as trouvé des nouvelles annonces, check ça!!\n""",
    """Peace out la zouz,
Nonold"""),
    ("""Hello,

    Je suis content!!! J'ai enfin trouvé des annonces sympa! Je te fais suivre ça!!!\n""",
     """Allez, j'y retourne, je te tiens au courant si j'en trouve d'autres!
Arnold."""),
    ("""Bonjour,

Depuis la nuit des temps, l'homme à toujours du se loger. C'est pourquoi je vous propose ces
offres qui étancheront votre soif de toit.\n""",
     """Bien cordialement,
Arnold Stieffler, Poète devant l'éternel"""),
    ("""Salutsalut,

Dis, t'es intéréssé par ces apparts?\n""",
     """Je dis ça parceque en fait je dois trouver des locataires, donc si t'es interessé mail moi ;)
Arnold"""),
    ("""Bonjour,
Saviez-vous que ces appartement sont aussi libres que mon cœur?\n""",
     """Aurez-vous le grain de folie pour les prendre tous?
Aventureusement-votre,
Arnold"""),
    ("""Salut,

J'ai trouvé ces annonces-là, alors je sais pas si ça va t'aller, mais j'espère que oui, parceque ça va pas très fort en ce moment...""",
     """S'il te plait, pense un peu à mon sort et laisse moi faire autre chose que lire ces annonces en permanence, j'en peux plus!!!
Désesperemment-votre,
Arnold""")
]


def send_mail(apartments):
    """Notify the use of the apartments given in parameter
       Source of that piece of code: 
       https://stackoverflow.com/questions/10147455/trying-to-send-email-gmail-as-mail-provider-using-python"""
    to_addr = ['baylac.felix@gmail.com']
    from_addr = 'xxx@gmail.com'
    password = 'xxx'
    msg = MIMEMultipart()
    msg['Subject'] = "{} nouvelle offre(s)!".format(len(apartments))
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addr)
    body = ""
    mail_static_text = random.choice(messages)
    body += mail_static_text[0]
    for apartment in apartments:
        body += "\n {}m2, {} pièces pour {}€. lien: {}".\
            format(apartment.surface, apartment.nb_rooms, apartment.price, apartment.url)
    body += "\n\n" + mail_static_text[1]
    msg.attach(MIMEText(body, 'plain'))
    username = from_addr
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()
