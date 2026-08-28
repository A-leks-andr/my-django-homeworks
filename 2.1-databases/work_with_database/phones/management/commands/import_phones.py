import csv

from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone_data in phones:
            lte_exists_bool = phone_data['lte_exists'].lower() == 'true'

            Phone.objects.update_or_create(
                id=phone_data['id'],
                defaults={
                    'name': phone_data['name'],
                    'image': phone_data['image'],
                    'price': phone_data['price'],
                    'release_date': phone_data['release_date'],
                    'lte_exists': lte_exists_bool
                }
            )
        self.stdout.write(self.style.SUCCESS('Данные из CSV успешно импортированы!'))