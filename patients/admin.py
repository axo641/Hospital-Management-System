from django.contrib import admin
from .models import Patient,Room

admin.site.register(Patient)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'status', 'capacity')
    list_filter = ('room_type', 'status')
    search_fields = ('room_number',)