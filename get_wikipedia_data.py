#!/use/bin/env python3
from typing import Dict, List
import wikipedia
import sys
import re

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

class Flower():
    def __init__(self, name: str, active_months: List[int], images: List[str]):
        self.name = name
        self.active_months = active_months
        self.images = images

    def __str__(self):
        return "Flower({}, \n{}, \n{})".format(self.name, self.active_months, self.images)

def get_flower_data(flower_name: str) -> Flower:
    flower = wikipedia.page(flower_name)
    name = flower.title
    page_html = flower.html()
    active_months = [int(i) for i in month_re.findall(page_html)]
    if len(active_months) == 0:
        active_months = list(range(1, 13)) # set as good for all months
    images = ([image for image in flower.images if not image.lower().endswith('.svg')])

    return Flower(name, active_months, images)

def run_main():
    wikipedia.set_lang('he')

    # get flower data from WIKIPEDIA
    for page in WIKI_MAIN_LINKS:
        wikipage = wikipedia.page(page)
        for flower_name in wikipage.links:
            try:
                flower = get_flower_data(flower_name)
            except(wikipedia.exceptions.PageError):
                continue
            print (flower)

    for page_id in PAGE_IDS:
        wikipage = wikipedia.page(pageid=page_id)
        for flower in wikipage.links:
            get_flower_data(flower)

        # for each flower link
        # flower = get_flower_data(flower: string)
        # store flower in db
        # grab image
    pass
if __name__ == '__main__':
    run_main()
