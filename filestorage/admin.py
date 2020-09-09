from django.contrib import admin

from filestorage.models import APIFile


class APIFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'original_filename', 'ext', 'file_type', 'file_sub_type', 'file_duration',
                    'created_at')


admin.site.register(APIFile, APIFileAdmin)
