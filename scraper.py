import urllib.request
import logging
import sys
import re
import database
import sqlite3
from bs4 import BeautifulSoup


def scrapItem(item_url):
        page = urllib.request.urlopen(item_url).read()
        soup = BeautifulSoup(page, 'html.parser')
        price = re.sub("\D", "", soup.find_all('span', 'price')[0].text)
        surface_label = soup.find_all('th', text='Surface : ')
        surface = surface_label[0].find_next_sibling().text
        surface = re.sub("m2", "", surface)
        zip_code = soup.find_all('th', text='Code postal :')[0].\
            find_next_sibling().text
        try:
            flat_type = soup.find_all('th', text='Meublé / Non meublé : ')[0].\
                find_next_sibling().text
        except:
            flat_type = None
        try:
            nb_rooms = soup.find_all('th', text='Pièces : ')[0].\
                find_next_sibling().text
        except:
            nb_rooms = None
        return database.Appartment(item_url, price, surface, zip_code,
                                   nb_rooms, flat_type)


def scrapPage(page_url):
    db_connection = sqlite3.connect('lbcScrap.sqlite3')
    db_cursor = db_connection.cursor()
    try:
        page = urllib.request.urlopen(page_url).read()
    except Exception as err:
        logging.critical('Cannot open the page url: ' + err)
        logging.critical('ABORDING.')
        sys.exit(1)
    soup = BeautifulSoup(page, 'html.parser')
    item_list = soup.find_all('div', 'list-lbc')[0]
    for item in item_list.find_all('a', href=True)[:-1]:
        url = item['href']
        if not database.Appartment.\
                appartment_already_in_db(db_cursor, url):
                appartment = scrapItem(url)
                appartment.save(db_cursor)
                print(url + " saved to db")
    db_connection.commit()
    db_connection.close()

page_url = "http://www.leboncoin.fr/locations/offres/ile_de_france/paris/?f=a&th=1&mre=1500&sqs=3"
logging.info("Updating database.")
scrapPage(page_url)
