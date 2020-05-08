#!/usr/bin/env python3
from typing import List
from pydal import DAL, Field
import sqlite3
import wikipedia
import sys
import re
sys.path.append('.')
from model import define_tables

WIKI_MAIN_LINKS = """
פורטל:בוטניקה/פרחי_ארץ_ישראל_לפי_צבעים/פרחים_אדומים
פורטל:בוטניקה/פרחי_ארץ_ישראל_לפי_צבעים/פרחים_כחולים
פורטל:בוטניקה/פרחי_ארץ_ישראל_לפי_צבעים/פרחים_סגולים
פורטל:בוטניקה/פרחי_ארץ_ישראל_לפי_צבעים/פרחים_ורודים
פורטל:בוטניקה/פרחי_ארץ_ישראל_לפי_צבעים/פרחים_לבנים
פורטל:בוטניקה/פרחי_ארץ_ישראל_לפי_צבעים/פרחים_צהובים
פורטל:בוטניקה/פרחי_ארץ_ישראל_לפי_צבעים/פרחים_בצבע_קרם
פורטל:בוטניקה/פרחי_ארץ_ישראל_לפי_צבעים/פרחים_חומים
פורטל:בוטניקה/פרחי_ארץ_ישראל_לפי_צבעים/פרחים_בצבע_ארגמן
פורטל:בוטניקה/פרחי_ארץ_ישראל_לפי_צבעים/פרחים_ירוקים
""".split()
PAGE_IDS = """1073632""".split()

# Yellow white flowers could not be addressed with the API. Using page
# ID to get them

month_re = re.compile('<td style="text-align: center; background-color:#90EE90; color:black;"><abbr title=[^ ]* class="wpAbbreviation">(1?[0-9])</abbr></td>')


db = DAL('sqlite://flower_storage.db', folder='./data')
define_tables(db)

class Flower():
    def __init__(self, name: str, active_months: List[int], images: List[str]):
        self.name = name
        self.active_months = active_months
        self.images = images

    def __str__(self):
        return "Flower('{}', \"{}\")".format(self.name, self.active_months)

def get_flower_data(flower_name: str) -> Flower:
    flower = wikipedia.page(flower_name)
    name = flower.title
    page_html = flower.html()
    active_months = [int(i) for i in month_re.findall(page_html)]
    if len(active_months) == 0:
        active_months = list(range(1, 13)) # set as good for all months
    images = ([image for image in flower.images if not image.lower().endswith('.svg')])

    return Flower(name, active_months, images)

def insert_flower_to_db(flower: Flower):
    ''' Inserts a flower record into the DB
    '''
    id = db.flowers.insert(name=flower.name,
                        is_month_1=1 in flower.active_months,
                        is_month_2=2 in flower.active_months,
                        is_month_3=3 in flower.active_months,
                        is_month_4=4 in flower.active_months,
                        is_month_5=5 in flower.active_months,
                        is_month_6=6 in flower.active_months,
                        is_month_7=7 in flower.active_months,
                        is_month_8=8 in flower.active_months,
                        is_month_9=9 in flower.active_months,
                        is_month_10=10 in flower.active_months,
                        is_month_11=11 in flower.active_months,
                        is_month_12=12 in flower.active_months)

    db.commit()
    print (flower)
    return id

def insert_image_urls_to_db(images, flower_id):
    for url in images:
        try:
            db.images.insert(url=url, flower_id=flower_id)
        except sqlite3.IntegrityError:
            print ("URL {} is allready inserted".format(url))

def handle_wikipage(wikipage):
    print ("Loading data from portal {}".format(wikipage.title))
    for flower_name in wikipage.links:
        try:
            flower = get_flower_data(flower_name)
        except(wikipedia.exceptions.PageError):
            continue
        try:
            flower_id = insert_flower_to_db(flower)
        except sqlite3.IntegrityError:
            print ("Flower {} is allready inserted".format(flower.name))
            flower_id = db(db.flowers.name == flower.name).select().first().id

        insert_image_urls_to_db(flower.images, flower_id)


def run_main():
    wikipedia.set_lang('he')
    define_tables()

    # get flower data from WIKIPEDIA
    for page in WIKI_MAIN_LINKS:
        handle_wikipage( wikipedia.page(page) )

    for page_id in PAGE_IDS:
        handle_wikipage( wikipedia.page(page) )

        # for each flower link
        # flower = get_flower_data(flower: string)
        # store flower in db
        # grab image
    pass
if __name__ == '__main__':
    run_main()
