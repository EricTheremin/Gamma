from .models import *


def get_pipeline_context():

    context_data = {}
    pipeline_data = []

    pip_qset = PipelineElement.objects.select_related('country', 'wbs', 'commodity', 'period')
    period_qset = Period.objects.all()
    country_qset = Country.objects.select_related('rb')
    rb_qset = RB.objects.all()
    wbs_qset = WBSElement.objects.select_related('country')
    commodity_qset = Commodity.objects.all()

    # period_qset = Period.objects.all()
    #
    # for wbs in wbs_qset:
    #     pipeline_data.append({
    #         'country_iso': wbs.country.iso_code,
    #         'wbs': wbs.code,
    #
    #     })
    #
    #
    # for pip in pip_qset:
    #     pipeline_data.append({
    #         'country_iso': pip.country.iso_code,
    #         'wbs': pip.wbs.code,
    #         'period': pip.period.date_start,
    #         'commodity': pip.commodity.name,
    #     })
    # context_data['pipeline'] = pipeline_data

    context_data['pipeline'] = pip_qset
    context_data['periods'] = period_qset.order_by('date_start')
    context_data['countries'] = country_qset
    context_data['rbs'] = rb_qset
    context_data['wbss'] = wbs_qset
    context_data['commodities'] = commodity_qset

    return context_data

