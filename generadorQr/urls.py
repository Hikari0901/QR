from django.urls import path
from . import views  # Asegúrate de que esto está importando correctamente tu vista

urlpatterns = [
    path('generate/', views.generate_qr_code, name='generate_qr_code'),
]
