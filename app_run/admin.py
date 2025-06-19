from django.contrib import admin

from app_run.models import Run


# Register your models here.
@admin.register(Run)
class RunModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'athlete', 'comment', 'created_at', 'status')
    ordering = ('created_at',)
    list_filter = ('athlete',)
    search_fields = ('athlete',)
    readonly_fields = ('status',)
