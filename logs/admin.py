from django.contrib import admin
from .models import Topic,Entry

class TopicAdmin(admin.ModelAdmin):
    list_display = ('text','date_added')
class EntryAdmin(admin.ModelAdmin):
    list_display = ('topic','text','date_added')

admin.site.register(Topic, TopicAdmin)
admin.site.register(Entry, EntryAdmin)

# Register your models here.
