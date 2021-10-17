import json
from os import name
import time
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse, response
import pandas as pd
from core.models import JailPopulation, SupplyData, Unit


def sec_to_min(seconds):
    """[returns time duration in minutes with 2 decimal floating point]

    Args:
        seconds ([float]): [time duration in seconds]

    Returns:
        [float]: [time duration in minutes]
    """
    return round(seconds/60, 2)


# Create your views here.
class VisualisationView(DetailView):
    template_name = 'visualisation/data_visualisation.html'
    context_object_name = 'client'

    def get_object(self, **kwargs):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # id = self.kwargs.get("id")

        client = self.request.user
        client_user_object = User.objects.get(id=client.id)
        name = f'{client_user_object.last_name}, {client_user_object.first_name}'

        context['client_name'] = name
        context['client_id'] = client.id

        return context


class DataUpload(View):
    def post(self, request):
        user = self.request.user
        data_file = request.FILES['data-file']

        if data_file.name.endswith('.csv'):
            data_df = pd.read_csv(data_file)
        elif data_file.name.endswith('.xls') or data_file.name.endswith('.xlsx'):
            data_df = pd.read_excel(data_file)

        for i in range(len(data_df)):
            try:
                name = data_df.loc[i, 'unit']
                log = data_df.loc[i, 'logdate']
                shift = data_df.loc[i, 'unit_shift']
                tencode = data_df.loc[i, 'tencode']
                tencode_complete_time = data_df.loc[i, 'Avg_Min']

                if pd.notnull(name) and pd.notnull(log) and pd.notnull(shift) and pd.notnull(tencode) and pd.notnull(tencode_complete_time):
                    # logs = Unit.objects.filter(
                    #     name=name, log=log, shift=shift, tencode=tencode, tencode_complete_time=tencode_complete_time, user=user)
                    # logs.delete()
                    Unit.objects.create(
                        name=name,
                        log=log,
                        shift=shift,
                        tencode=tencode,
                        tencode_complete_time=tencode_complete_time,
                        user=user
                    )
                    status = 201
                else:
                    status = 403
            except:
                date = data_df.loc[i, 'Date']
                count_population = data_df.loc[i, 'Count Population']

                if pd.notnull(date) and pd.notnull(count_population):
                    jail_populations = JailPopulation.objects.filter(
                        user=user, date=date, count_population=count_population)
                    jail_populations.delete()
                    JailPopulation.objects.create(
                        user=user,
                        date=date,
                        count_population=count_population
                    )
                    status = 201
                else:
                    status = 403

        return JsonResponse({'status': status})


class PlotData(View):
    def get(self, request):
        user = self.request.user
        unit_list = json.loads(request.GET.get('unit_list', ''))
        if len(unit_list) == 0:
            unit_list = ['A1', 'A11', 'A3', 'A4', 'A10',
                         'B10', 'B11', 'B1', 'B2', 'B3', 'C10']
        tencode_list = json.loads(request.GET.get('tencode_list', ''))
        # data = []
        usage_data = {}

        if Unit.objects.filter(user=user).exists():
            enrt = 0.0
            arrvd = 0.0
            ajail = 0.0
            cmplt = 0.0
            if len(tencode_list) == 0:
                for unit in unit_list:
                    enrt_queryset = Unit.objects.filter(name=unit, user=user,
                                                        tencode='ENRT')
                    arrvd_queryset = Unit.objects.filter(name=unit, user=user,
                                                         tencode='ARRVD')
                    ajail_queryset = Unit.objects.filter(name=unit, user=user,
                                                         tencode='AJAIL')
                    cmplt_queryset = Unit.objects.filter(name=unit, user=user,
                                                         tencode='CMPLT')
                    for query in enrt_queryset:
                        enrt = enrt + float(query.tencode_complete_time)
                    for query in arrvd_queryset:
                        arrvd = arrvd + float(query.tencode_complete_time)
                    for query in ajail_queryset:
                        ajail = ajail + float(query.tencode_complete_time)
                    for query in cmplt_queryset:
                        cmplt = cmplt + float(query.tencode_complete_time)

                logs = Unit.objects.filter(user=user)
                if logs:
                    total_tencode_time = 0
                    for log in logs:
                        total_tencode_time = total_tencode_time + \
                            float(log.tencode_complete_time)
                    enrt_usage_percent = round(
                        (enrt/total_tencode_time) * 100, 2)
                    arrvd_usage_percent = round(
                        (arrvd/total_tencode_time) * 100, 2)
                    ajail_usage_percent = round(
                        (ajail/total_tencode_time) * 100, 2)
                    cmplt_usage_percent = round(
                        (cmplt/total_tencode_time) * 100, 2)

                usage_data = {'enrt_usage_percent': enrt_usage_percent, 'arrvd_usage_percent': arrvd_usage_percent,
                              'ajail_usage_percent': ajail_usage_percent, 'cmplt_usage_percent': cmplt_usage_percent,
                              }
            else:
                tencode_query_dict = {}
                usage_data = {}
                enrt = 0.0
                arrvd = 0.0
                ajail = 0.0
                cmplt = 0.0
                for tencode in tencode_list:
                    query_list = []
                    for unit in unit_list:
                        query_list.append(Unit.objects.filter(name=unit, user=user,
                                                              tencode=tencode))
                    tencode_query_dict[tencode] = query_list
                logs = Unit.objects.filter(user=user)
                if logs:
                    total_tencode_time = 0
                    for log in logs:
                        total_tencode_time = total_tencode_time + \
                            float(log.tencode_complete_time)

                for tencode in tencode_list:
                    if tencode in tencode_query_dict:
                        enrt = 0
                        enrt_query_list = tencode_query_dict[tencode]
                        for item in enrt_query_list:
                            enrt_queryset = item
                        for query in enrt_queryset:
                            enrt = enrt + float(query.tencode_complete_time)
                        enrt_usage_percent = round(
                            (enrt/total_tencode_time) * 100, 2)
                        usage_data[tencode.lower() +
                                   '_usage_percent'] = enrt_usage_percent

                    # elif 'ARRVD' in tencode_query_dict:
                    #     arrvd_query_list = tencode_query_dict['ARRVD']
                    #     for item in arrvd_query_list:
                    #         arrvd_queryset = item
                    #     for query in arrvd_queryset:
                    #         arrvd = arrvd + float(query.tencode_complete_time)
                    #     arrvd_usage_percent = round(
                    #         (arrvd/total_tencode_time) * 100, 2)
                    #     usage_data['arrvd_usage_percent'] = arrvd_usage_percent
                    # elif 'AJAIL' in tencode_query_dict:
                    #     ajail_query_list = tencode_query_dict['AJAIL']
                    #     for item in ajail_query_list:
                    #         ajail_queryset = item
                    #     for query in ajail_queryset:
                    #         ajail = ajail + float(query.tencode_complete_time)
                    #     ajail_usage_percent = round(
                    #         (ajail/total_tencode_time) * 100, 2)
                    #     usage_data['ajail_usage_percent'] = ajail_usage_percent
                    # elif 'CMPLT' in tencode_query_dict:
                    #     cmplt_query_list = tencode_query_dict['CMPLT']
                    #     for item in cmplt_query_list:
                    #         cmplt_queryset = item
                    #     for query in cmplt_queryset:
                    #         cmplt = cmplt + float(query.tencode_complete_time)
                    #     cmplt_usage_percent = round(
                    #         (cmplt/total_tencode_time) * 100, 2)
                    #     usage_data['cmplt_usage_percent'] = cmplt_usage_percent

            response = 200
            usage_data['response'] = response
        else:
            response = 403
            usage_data['response'] = response

        return JsonResponse(usage_data)


class PlotAverageTencodeSpent(View):
    def get(self, request):
        user = self.request.user
        total_tencode_time_a1 = 0
        total_tencode_time_a11 = 0
        total_tencode_time_a3 = 0
        total_tencode_time_a10 = 0
        total_tencode_time_a4 = 0
        total_tencode_time_b1 = 0
        total_tencode_time_b2 = 0
        total_tencode_time_b3 = 0
        total_tencode_time_b10 = 0
        total_tencode_time_b11 = 0
        total_tencode_time_c10 = 0

        # Average spent time on tencode
        unit_a1_logs = Unit.objects.filter(name='A1', user=user)
        unit_a11_logs = Unit.objects.filter(name='A11', user=user)
        unit_a3_logs = Unit.objects.filter(name='A3', user=user)
        unit_a10_logs = Unit.objects.filter(name='A10', user=user)
        unit_a4_logs = Unit.objects.filter(name='A4', user=user)
        unit_b1_logs = Unit.objects.filter(name='B1', user=user)
        unit_b2_logs = Unit.objects.filter(name='B2', user=user)
        unit_b3_logs = Unit.objects.filter(name='B3', user=user)
        unit_b10_logs = Unit.objects.filter(name='B10', user=user)
        unit_b11_logs = Unit.objects.filter(name='B11', user=user)
        unit_c10_logs = Unit.objects.filter(name='C10', user=user)

        if unit_a1_logs:
            for log in unit_a1_logs:
                total_tencode_time_a1 = total_tencode_time_a1 + \
                    float(log.tencode_complete_time)
            a1_avg_time_spent = total_tencode_time_a1 / unit_a1_logs.count()

        if unit_a11_logs:
            for log in unit_a11_logs:
                total_tencode_time_a11 = total_tencode_time_a11 + \
                    float(log.tencode_complete_time)
            a11_avg_time_spent = total_tencode_time_a11 / unit_a11_logs.count()

        if unit_a3_logs:
            for log in unit_a3_logs:
                total_tencode_time_a3 = total_tencode_time_a3 + \
                    float(log.tencode_complete_time)
            a3_avg_time_spent = total_tencode_time_a3 / unit_a3_logs.count()

        if unit_a10_logs:
            for log in unit_a10_logs:
                total_tencode_time_a10 = total_tencode_time_a10 + \
                    float(log.tencode_complete_time)
            a10_avg_time_spent = total_tencode_time_a10 / unit_a10_logs.count()

        if unit_a4_logs:
            for log in unit_a4_logs:
                total_tencode_time_a4 = total_tencode_time_a4 + \
                    float(log.tencode_complete_time)
            a4_avg_time_spent = total_tencode_time_a4 / unit_a4_logs.count()

        if unit_b1_logs:
            for log in unit_b1_logs:
                total_tencode_time_b1 = total_tencode_time_b1 + \
                    float(log.tencode_complete_time)
            b1_avg_time_spent = total_tencode_time_b1 / unit_b1_logs.count()

        if unit_b2_logs:
            for log in unit_b2_logs:
                total_tencode_time_b2 = total_tencode_time_b2 + \
                    float(log.tencode_complete_time)
            b2_avg_time_spent = total_tencode_time_b2 / unit_b2_logs.count()

        if unit_b3_logs:
            for log in unit_b3_logs:
                total_tencode_time_b3 = total_tencode_time_b3 + \
                    float(log.tencode_complete_time)
            b3_avg_time_spent = total_tencode_time_b3 / unit_b3_logs.count()

        if unit_b10_logs:
            for log in unit_b10_logs:
                total_tencode_time_b10 = total_tencode_time_b10 + \
                    float(log.tencode_complete_time)
            b10_avg_time_spent = total_tencode_time_b10 / unit_b10_logs.count()

        if unit_b11_logs:
            for log in unit_b11_logs:
                total_tencode_time_b11 = total_tencode_time_b11 + \
                    float(log.tencode_complete_time)
            b11_avg_time_spent = total_tencode_time_b11 / unit_b11_logs.count()

        if unit_c10_logs:
            for log in unit_c10_logs:
                total_tencode_time_c10 = total_tencode_time_c10 + \
                    float(log.tencode_complete_time)
            c10_avg_time_spent = total_tencode_time_c10 / unit_c10_logs.count()

        return JsonResponse({'a1_avg_time_spent': a1_avg_time_spent,
                             'a11_avg_time_spent': a11_avg_time_spent,
                             'a3_avg_time_spent': a3_avg_time_spent,
                             'a10_avg_time_spent': a10_avg_time_spent,
                             'a4_avg_time_spent': a4_avg_time_spent,
                             'b1_avg_time_spent': b1_avg_time_spent,
                             'b2_avg_time_spent': b2_avg_time_spent,
                             'b3_avg_time_spent': b3_avg_time_spent,
                             'b10_avg_time_spent': b10_avg_time_spent,
                             'b11_avg_time_spent': b11_avg_time_spent,
                             'c10_avg_time_spent': c10_avg_time_spent})


class UploadSupplierData(View):
    def post(self, request):
        user = self.request.user

        user = self.request.user
        data_file = request.FILES['data-file']

        if data_file.name.endswith('.csv'):
            data_df = pd.read_csv(data_file)
        elif data_file.name.endswith('.xls') or data_file.name.endswith('.xlsx'):
            data_df = pd.read_excel(data_file)
        for i in range(len(data_df)):
            supplier_name = data_df.loc[i, 'Supplier Name']
            paid_year = data_df.loc[i, 'Paid Date FY Year']
            total_net_amount = data_df.loc[i, 'Total Net Amount']

            if pd.notnull(supplier_name) and pd.notnull(paid_year) and pd.notnull(total_net_amount):
                suppliers = SupplyData.objects.filter(
                    user=user, supplier_name=supplier_name, paid_year=paid_year, total_net_amount=total_net_amount)

                # suppliers.delete()

                SupplyData.objects.create(
                    user=user,
                    supplier_name=supplier_name,
                    paid_year=paid_year,
                    total_net_amount=total_net_amount
                )
                status = 201
            else:
                status = 403
        return JsonResponse({'status': status})


class PlotJailPopulation(View):
    def get(self, request):
        user = self.request.user
        date = []
        count_population = []
        if not user.is_anonymous:
            jail_populations = JailPopulation.objects.filter(user=user)
            if jail_populations:
                for jail_population in jail_populations:
                    date.append(jail_population.date)
                    count_population.append(jail_population.count_population)
                status = 200
            else:
                status = 404
        else:
            status = 401

        return JsonResponse({'date': date, 'count_population': count_population, 'status': status})


class FetchSupplierName(View):
    def get(self, request):
        client_id = request.GET.get('client_id', None)

        user = User.objects.get(id=client_id)
        data = []
        if user:
            suppliers = SupplyData.objects.filter(
                user=user).distinct('supplier_name')
            print(suppliers.count())
            for supplier in suppliers:
                data.append({
                    'supplier_name': supplier.supplier_name
                })
            print(data)
        return JsonResponse(data, safe=False)


class FetchSupplierData(View):
    def get(self, request):
        supplier_name = request.GET.get('supplier_name', None)

        supplier_datas = SupplyData.objects.filter(supplier_name=supplier_name)
        data = []
        for supplier_data in supplier_datas:
            data.append({
                'paid_year': supplier_data.paid_year,
                'total_net_amount': supplier_data.total_net_amount
            })
        print(data)
        return JsonResponse(data, safe=False)
