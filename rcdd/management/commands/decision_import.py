import base64
import bs4
import csv
import http
import re
import requests
from bs4 import BeautifulSoup
from datetime import *
from dateutil.parser import *
from dateutil.tz import *
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils import timezone
from urllib.request import urlopen

from rcdd.models import Court
from rcdd.models import Court, Decision

DEFAULT = datetime(2003, 9, 25)


def san(string):
    return re.sub(r"[\n\t\s]*", "", string).strip()


class Command(BaseCommand):
    """ For every court, fetch court decisions and save to db"""
    courts = Court.objects.all()
    for c in courts:
        url = c.web_adress
        page = requests.get(url, verify=False)
        soup = BeautifulSoup(page.content, 'html.parser')
        tables = soup.find_all("tbody")
        decision_table = soup.find("table", {'class': 'views-table'})
        try:
            decision_table_body = table1.find('tbody')
        except AttributeError:
            print('court ', url, 'cannot find decision table!')

        decision_table_rows = table2.find_all('tr')

        for row in decision_table_rows:
            court = Court.objects.get(name_short="jbl")
            cells = row.find_all("td")
            file_number = san(cells[0].get_text())
            date_pron = san(cells[1].get_text())
            date_created = san(cells[2].get_text())
            date_published = san(cells[3].get_text())
            file_name = cells[4].get_text()
            file_type = cells[5].get_text()
            file_theme = cells[6].get_text()
            file_base64 = cells[7].find_all("input", {'name': 'my_base64'})[0].get('value')
            file = base64.b64decode(file_base64).decode('utf-16')
            # date pron can be missing, depending on the decision! dateutil.parser.parse('') == current date!
            if date_pron:
                d = Decision(court=court, file_number=file_number, date_pron=parse(date_pron, dayfirst=True),
                             date_created=parse(date_created, dayfirst=True),
                             date_published=parse(date_published, dayfirst=True),
                             file_name=file_name, file_type=file_type, file_theme=file_theme, file=file)
            else:
                d = Decision(court=court, file_number=file_number, date_created=parse(date_created, dayfirst=True),
                             date_published=parse(date_published, dayfirst=True),
                             file_name=file_name, file_type=file_type, file_theme=file_theme, file=file)
            try:
                d.save()
            except IntegrityError:
                print('dec present in DB!')

    def handle(self, *args, **options):
        pass
