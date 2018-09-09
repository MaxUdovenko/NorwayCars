from django.shortcuts import render, HttpResponse
import pandas as pd
from django.contrib.staticfiles.storage import staticfiles_storage

import plotly.graph_objs as go
from plotly.offline import plot
import plotly.utils as pu

from django.http import JsonResponse
import json


def pandas_table(request):
    cars_df = cars_list()
    return render(request, 'pandas_table.html', {'cars_df': cars_df})


def cars_list():
    csv_file = staticfiles_storage.path('csv/norway_new_car_sales_by_make.csv')
    df = pd.read_csv(csv_file)

    cars_df = df['Make'].unique()

    return cars_df


def statistics_by_car_name(request):

    car_name = request.POST['car_name']
    cars_df = cars_list()

    csv_file = staticfiles_storage.path('csv/norway_new_car_sales_by_make.csv')
    df = pd.read_csv(csv_file)

    df_years = df['Year'].unique()

    # Quantity list
    q_list = list()
    for item in df_years:
        q_list.append(df.loc[df['Year'] == item].loc[df['Make'] == car_name]['Quantity'].sum())

    # Plotly part
    trace1 = go.Scatter(x=df_years, y=q_list, name=car_name)
    data = [trace1]

    fig = go.Figure(data=data)

    final_data = json.loads( json.dumps(fig, cls=pu.PlotlyJSONEncoder) )

    return JsonResponse(final_data, safe=False)

