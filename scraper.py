import argparse
import urllib.request
import logging
import sys
import re
import database
import sqlite3
import mail
from bs4 import BeautifulSoup


def scrapItem(item_url):
    page = urllib.request.urlopen(item_url).read()
    soup = BeautifulSoup(page, 'html.parser')
    elems = soup.find_all('span', 'value')
    price = re.sub("\D", "", [x.text for x in elems if "€" in x.text][0])
    surface = re.sub(" m2", "", [x.text for x in elems if 'm2' in x.text][0])
    try:
        flat_type = [x.text for x in elems if x.text in ['Non meublé', 'Meublé']][0]
    except:
        flat_type = None
    try:
        nb_rooms = [x.text for x in elems if x.text.isdigit()][0]
    except:
        nb_rooms = None
    return database.Appartment(item_url, price, surface,
                               nb_rooms, flat_type)


def scrapPage(page_url, db_url):
    db_connection = sqlite3.connect(db_url)
    db_cursor = db_connection.cursor()
    flats = []
    try:
        page = urllib.request.urlopen(page_url).read()
    except Exception as err:
        logging.critical('Cannot open the page url: ' + err)
        logging.critical('ABORDING.')
        sys.exit(1)
    soup = BeautifulSoup(page, 'html.parser')
    item_list = soup.find_all('section', 'tabsContent')[0]
    for item in item_list.find_all('a', href=True)[:-1]:
        url = "http:" + item['href']
        if not database.Appartment. \
                appartment_already_in_db(db_cursor, url):
            appartment = scrapItem(url)
            appartment.save(db_cursor)
            flats.append(appartment)
            print(url + " saved to db")
            db_connection.commit()
    db_connection.close()
    if len(flats) > 0:
        mail.send_mail(flats)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', metavar='URL', type=str, help="Le bon coin page url you want to parse.")
    parser.add_argument('DB_URL', help='SQLite database path.')
    parser.add_argument('--create-tables', action='store_true', help="Creates database tables.")
    args = parser.parse_args()
    page_url = args.url
    db_url = args.DB_URL
    if args.create_tables:
        database.Appartment.createDB(db_url)
        logging.info("Appartments table succesfully created.")
    logging.info("Updating database.")
    scrapPage(page_url, db_url)
