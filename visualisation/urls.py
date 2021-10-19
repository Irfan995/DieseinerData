from os import name
from django.urls import path

from core.models import SupplyData
from . views import FetchSupplierData, FetchSupplierName, PlotJailPopulation, UploadSupplierData, VisualisationView, DataUpload, PlotData, PlotAverageTencodeSpent


app_name = 'visualisation'

urlpatterns = [
    path('data-visualisation/', VisualisationView.as_view(),
         name='data-visualisation'),
    path('data-upload/', DataUpload.as_view(), name='data-upload'),
    path('supplier-data-upload/', UploadSupplierData.as_view(),
         name='supplier-data-upload'),
    path('plot-data/', PlotData.as_view(), name='plot-data'),
    path('plot-avg-tencode-spent/', PlotAverageTencodeSpent.as_view(),
         name='plot-avg-tencode-spent'),
    path('plot-jail-population-data/', PlotJailPopulation.as_view(),
         name='plot-jail-population-data'),

    path('fetch-supplier-name/', FetchSupplierName.as_view(),
         name='fetch-supplier-name'),
    path('fetch-supplier-data/', FetchSupplierData.as_view(),
         name='fetch-supplier-data'),
]
