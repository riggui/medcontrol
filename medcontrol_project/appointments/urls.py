from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('documents/', views.DocumentListView.as_view(), name='documents'),
    path('athletes/', views.AthleteListView.as_view(), name='athlete_list'),
    path('reserve/<int:creneau_id>/', views.reserve_creneau, name='reserve_creneau'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('api/creneaux/', views.creneaux_json, name='creneaux_json'),
    path('reserver/<int:creneau_id>/', views.reserver_creneau, name='reserver_creneau'),
    path('api/reserver/<int:creneau_id>/', views.api_reserver, name='api_reserver'),
]
