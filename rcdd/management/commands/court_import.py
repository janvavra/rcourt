from django.core.management.base import BaseCommand
from django.utils import timezone
import csv
from rcdd.models import Court
from django.db import IntegrityError



class Command(BaseCommand):
    """ Import courts to DB from txt file"""
    with open('courts.txt', newline='', encoding='utf-16') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for row in reader:
            name = row[0]
            name_short = row[1]
            web_adress = row[2]
            c = Court(name=name, name_short=name_short, web_adress=web_adress)
            try:
                c.save()
            except IntegrityError:
                print("court name:", name, 'duplicate in db!')

    def handle(self, *args, **options):
        pass
