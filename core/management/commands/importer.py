from decimal import Decimal
from pprint import pprint

import time
from os import listdir
import json
from os.path import isfile, join

from django.core.management.base import BaseCommand

from core.models import Company


class Command(BaseCommand):

    def handle(self, *args, **options):
        files = listdir('project/import')

        print(files)

        for file_ in files:
            with open(f'project/import/{file_}', 'r') as f:
                json_data = json.loads(f.read())
                print(json_data['inn'])

                if json_data['inn'] == '7743225631':
                    continue

                try:
                    Company.objects.get_or_create(
                        inn=json_data['inn'],
                        defaults={
                            'ogrn': json_data['ogrn'],
                            'company_name': json_data['companyName'],
                            'company_short_name': json_data['companyShortName'],
                            'revenue_2019': json_data['revenue2019'],
                            'revenue_2018': json_data['revenue2018'],
                            'revenue_growth': json_data['revenueGrowth'],
                            'revenue_growth_perc': json_data['revenueGrowthPerc'],
                            'purchases_wins': json_data['purchasesWins'],
                            'purchases_total': json_data['purchasesTotal'],
                            'purchases_lost': json_data['purchasesLost'],
                            'revenue_lost': json_data['revenueLost'],
                            'bg_overpayment_perc': json_data['bgOverpaymentPerc'],
                            'bg_sum': json_data['contractsSum'],
                            'competitor_inn': json_data['competitor']['inn'],
                            'competitor_ogrn': json_data['competitor']['ogrn'],
                            'competitor_full_name': json_data['competitor']['companyName'] or '',
                            'competitor_short_name': json_data['competitor']['companyShortName'] or '',
                            'competitor_growth_percent': json_data['competitor']['revenueGrowthPerc'],
                            'competitor_purchases_wins': json_data['competitor']['purchasesWins'],
                            'competitor_purchases_total': json_data['competitor']['purchasesTotal'],
                            'competitor_bg_saving_economy': int(json_data['competitor']['bgSavingEconomy']),
                            # '': json_data['competitor']['contractsSum'],
                        }
                    )
                except KeyError:
                    continue
                except Exception as e:
                    pprint(json_data)
                    print(json_data['inn'], e)
                    raise e

