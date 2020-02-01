import csv
from .models import *
from datetime import datetime
from gamma import constants
from gamma.utils import *


def load_periods():

    Period.objects.all().delete()
    period_list = []

    with open(load_csv("Periods.csv", __file__), mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            date_str = row["period"]
            period_start_date = datetime.strptime(date_str, constants.DATE_FORMAT).date()
            period = Period(date_start=period_start_date)
            period_list.append(period)
            line_count += 1
        print(f'Processed {line_count} lines.')
        Period.objects.bulk_create(period_list)
        print(Period.objects.all())


def load_rbs():

    RB.objects.all().delete()
    rb_list = []

    with open(load_csv("RBs.csv", __file__), mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            rb = RB(name=row["RB"])
            rb_list.append(rb)
            line_count += 1
        print(f'Processed {line_count} lines.')
        RB.objects.bulk_create(rb_list)
        print(RB.objects.all())


def load_countries():

    Country.objects.all().delete()
    country_list = []

    rb_qset = RB.objects.all()

    with open(load_csv("Countries.csv", __file__), mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            country = Country(iso_code=row["iso_code"], co_code=row["co_code"], name=row["country"], rb=rb_qset.get(name=row["RB"]))
            country_list.append(country)
            line_count += 1
        print(f'Processed {line_count} lines.')
        Country.objects.bulk_create(country_list)
        print(Country.objects.all())


def load_wbs():

    WBSElement.objects.all().delete()
    wbs_list = []

    country_qset = Country.objects.all()

    with open(load_csv("WBS_elements.csv", __file__), mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            try:
                country_ = country_qset.get(co_code=row["office_code"])
            except Country.DoesNotExist:
                print('Country CO not found {}'.format(row["office_code"]))
            else:
                wbs = WBSElement(code=row["wbs_element"], country=country_)
                wbs_list.append(wbs)
                line_count += 1
        print(f'Processed {line_count} lines.')
        WBSElement.objects.bulk_create(wbs_list)
        print(WBSElement.objects.all())


def load_commodities():

    Commodity.objects.all().delete()
    com_list = []

    with open(load_csv("Commodities.csv", __file__), mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            com = Commodity(name=row["Commodity"], planning_name=row["Planning commodity"])
            com_list.append(com)
            line_count += 1
        print(f'Processed {line_count} lines.')
        Commodity.objects.bulk_create(com_list)
        print(Commodity.objects.all())


def load_pipeline():

    PipelineElement.objects.all().delete()
    pipeline_list = []

    country_qset = Country.objects.all()
    wbs_qset = WBSElement.objects.all()
    com_qset = Commodity.objects.all()
    period_qset = Period.objects.all()

    with open(load_csv("Pipeline.csv", __file__), mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            try:
                country_ = country_qset.get(co_code=row["office_code"])
                wbs_ = wbs_qset.get(code=row["wbs_element"])
                com_ = com_qset.get(name=row["commodity"])
                date_str = row["period"]
                period_start_date = datetime.strptime(date_str, constants.DATE_FORMAT).date()
                period_ = period_qset.get(date_start=period_start_date)
            except Country.DoesNotExist:
                print('Country CO not found {}'.format(row["office_code"]))
            except WBSElement.DoesNotExist:
                print('WBS Element not found {}'.format(row["wbs_element"]))
            except Commodity.DoesNotExist:
                print('Commodity not found {}'.format(row["commodity"]))
            except Period.DoesNotExist:
                print('Period not found {}'.format(row["period"]))
            else:
                pip = PipelineElement(country=country_,
                                      wbs=wbs_,
                                      commodity=com_,
                                      period=period_,
                                      implementation_reqs_mt=float(row["Implementation Reqs"]),
                                      implementation_shortfalls_mt=float(row["Implementation Shortfalls"]),
                                      implementation_reqs_fcr=float(row["Implementation Reqs FCR"]),
                                      implementation_shortfalls_fcr=float(row["Implementation Shortfalls FCR"])
                                      )
                pip.implementation_resourced_mt = pip.implementation_reqs_mt - pip.implementation_shortfalls_mt
                pip.implementation_resourced_fcr = pip.implementation_reqs_fcr - pip.implementation_shortfalls_fcr
                pipeline_list.append(pip)
                line_count += 1
        print(f'Processed {line_count} lines.')
        PipelineElement.objects.bulk_create(pipeline_list)
        print(PipelineElement.objects.all())
