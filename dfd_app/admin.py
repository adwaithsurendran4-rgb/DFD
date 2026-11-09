from django.contrib import admin
from .models import Project, Diagram, DFDTemplate, ForensicScan


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'notation_style', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('notation_style', 'created_at')


@admin.register(Diagram)
class DiagramAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'level', 'created_at', 'updated_at')
    list_filter = ('level', 'created_at')
    search_fields = ('name', 'project__name')


@admin.register(DFDTemplate)
class DFDTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'slug', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'summary', 'category')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ForensicScan)
class ForensicScanAdmin(admin.ModelAdmin):
    list_display = ('title', 'verdict', 'deepfake_score', 'source_type', 'created_at')
    list_filter = ('verdict', 'source_type', 'created_at')
    search_fields = ('title', 'source_url')
