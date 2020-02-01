import csv
from .models import *
from datetime import datetime
from gamma import constants
from gamma.utils import *


def load_supply_lines():

    SupplyLine.objects.all().delete()
    sl_list = []

    with open(load_csv("GCMF Supply Lines.csv", __file__), mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            sl = SupplyLine(name=row["Supply Line"])
            sl_list.append(sl)
            line_count += 1
        print(f'Processed {line_count} lines.')
        SupplyLine.objects.bulk_create(sl_list)
        print(SupplyLine.objects.all())


def load_corridors():

    supply_line_qset = SupplyLine.objects.all()
    Corridor.objects.all().delete()
    cor_list = []

    with open(load_csv("GCMF Corridors.csv", __file__), mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            try:
                supply_line_ = supply_line_qset.get(name=row["Supply Line"])
            except SupplyLine.DoesNotExist:
                print('SupplyLine not found {}'.format(row["Supply Line"]))
            else:
                cor = Corridor(name=row["Corridor"], supply_line=supply_line_)
                cor_list.append(cor)
                line_count += 1
        print(f'Processed {line_count} lines.')
        Corridor.objects.bulk_create(cor_list)
        print(Corridor.objects.all())


def load_gcmf_commodities():

    corridor_qset = Corridor.objects.all()
    commodity_qset = Commodity.objects.all()
    CommodityInCorridor.objects.all().delete()
    cic_list = []

    with open(load_csv("GCMF Commodities.csv", __file__), mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            try:
                corridor_ = corridor_qset.get(name=row["Corridor"])
                com_ = commodity_qset.get(name=row["Commodity"])
            except Corridor.DoesNotExist:
                print('Corridor not found {}'.format(row["Corridor"]))
            except Commodity.DoesNotExist:
                print('Commodity not found {}'.format(row["Commodity"]))
            else:
                if row["GCMF commodity"] == "1":
                    cic = CommodityInCorridor(corridor=corridor_, commodity=com_, is_gcmf_commodity=True)
                    cic_list.append(cic)
                    line_count += 1
        print(f'Processed {line_count} lines.')
        CommodityInCorridor.objects.bulk_create(cic_list)
        print(CommodityInCorridor.objects.all())


