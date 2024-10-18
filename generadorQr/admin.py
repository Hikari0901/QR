from django.contrib import admin
from .models import QRCode
# Define una clase personalizada para la vista del modelo en el admin
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'created_at')  # Campos que quieres mostrar en la lista de objetos
    search_fields = ('code',)  # Añade un campo de búsqueda para el código alfanumérico
    list_filter = ('created_at',)  # Filtros por fecha de creación
    readonly_fields = ('created_at',)  # Los campos que no pueden ser editados

# Registra el modelo con su clase personalizada
admin.site.register(QRCode, QRCodeAdmin)
