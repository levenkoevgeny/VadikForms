from django.contrib import admin
from .models import *


admin.site.register(Subject)
admin.site.register(Testing)
admin.site.register(Question)
admin.site.register(Answer)


@admin.register(Subdivision)
class GuidePageAdmin(admin.ModelAdmin):
    list_display = ('subdivision_name', 'user')
    list_display_links = ('subdivision_name',)
    list_filter = ('subdivision_name',)
    search_fields = ['subdivision_name',]