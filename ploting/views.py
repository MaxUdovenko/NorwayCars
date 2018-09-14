from django.shortcuts import render
import pandas as pd
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import JsonResponse
import json
import plotly.utils as pu


def pandas_table(request):
    car_makers = cars_makers_list()
    return render(request, 'car_makers.html', {'car_makers': car_makers})


def cars_makers_list():
    csv_file = staticfiles_storage.path('csv/norway_new_car_sales_by_make.csv')
    df = pd.read_csv(csv_file)

    car_makers = df['Make'].unique()

    return car_makers


def statistics_by_car_maker(request):

    car_name = request.POST['car_name']

    csv_file = staticfiles_storage.path('csv/norway_new_car_sales_by_make.csv')
    df = pd.read_csv(csv_file)

    df_years = df['Year'].unique()

    # Quantity list
    q_list = list()
    for item in df_years:
        q_list.append(df.loc[df['Year'] == item].loc[df['Make'] == car_name]['Quantity'].sum())

    data_for_plotly = {
        'name': car_name,
        'x': df_years,
        'y': q_list,
        'years': df_years
    }

    final_data = json.loads( json.dumps(data_for_plotly, cls=pu.PlotlyJSONEncoder) )

    return JsonResponse(final_data, safe=False)
