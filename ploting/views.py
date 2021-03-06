from django.shortcuts import render
import pandas as pd
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import JsonResponse
import json
import plotly.utils as pu


def pandas_table(request):
    csv_file = staticfiles_storage.path('csv/norway_new_car_sales_by_make.csv')
    df = pd.read_csv(csv_file)

    car_makers = df['Make'].unique()
    return render(request, 'car_makers.html', {'car_makers': car_makers})


def statistics_by_car_maker(request):

    car_name = request.POST['car_name']

    csv_file = staticfiles_storage.path('csv/norway_new_car_sales_by_make.csv')
    df = pd.read_csv(csv_file)

    # Selection by given car name
    dff = df[df['Make'] == car_name]

    # Dictionary for Plotly
    data_for_plotly = {
        'name': car_name,
        'x': dff.groupby('Year', as_index=False)['Quantity'].sum()['Year'].values.tolist(),
        'y': dff.groupby('Year', as_index=False)['Quantity'].sum()['Quantity'].values.tolist(),
    }

    # Convert data to Plotly format
    final_data = json.loads(json.dumps(data_for_plotly, cls=pu.PlotlyJSONEncoder))

    return JsonResponse(final_data, safe=False)
