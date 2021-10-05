from django.urls import path
from . views import PlotJailPopulation, VisualisationView, DataUpload, PlotData, PlotAverageTencodeSpent


app_name = 'visualisation'

urlpatterns = [
    path('data-visualisation/', VisualisationView.as_view(), name='data-visualisation'),
    path('data-upload/', DataUpload.as_view(), name='data-upload'),
    path('plot-data/', PlotData.as_view(), name='plot-data'),
    path('plot-avg-tencode-spent/',PlotAverageTencodeSpent.as_view(), name='plot-avg-tencode-spent'),
    path('plot-jail-population-data/', PlotJailPopulation.as_view(), name='plot-jail-population-data')
]