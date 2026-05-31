from django.urls import path
from . import views

urlpatterns = [
    path('', views.machine_list, name='machine_list'),
    path('machine/<int:machine_id>/', views.machine_detail, name='machine_detail'),
    path('simulation/<int:execution_id>/', views.simulation_step, name='simulation_step'),
]