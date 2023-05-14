from django.contrib import admin
from .models import List, Record

# Register your models here.
class ListAdmin(admin.ModelAdmin):
    list_display=['DateTime', 'Car', 'Detail', 'Location']

class RecordAdmin(admin.ModelAdmin):
    list_display = ['Active', 'IP', 'Content', 'Member', 'DateTime']

admin.site.register(List, ListAdmin)
admin.site.register(Record, RecordAdmin)