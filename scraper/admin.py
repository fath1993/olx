from django.contrib import admin
from scraper.models import Settings, JobLink, Job


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = (
        'scraper_active',
        'translated_language',
    )

    fields = (
        'scraper_active',
        'translated_language',
    )

    def has_add_permission(self, request):
        if Settings.objects.all().exists():
            return False


@admin.register(JobLink)
class JobLinkAdmin(admin.ModelAdmin):
    list_display = (
        'link',
    )

    fields = (
        'link',
    )


@admin.register(JobLink)
class JobLinkAdmin(admin.ModelAdmin):
    list_display = (
        'link',
    )

    fields = (
        'link',
    )


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        'source',
        'title_translation',
        'company',
        'city',
        'date',
    )

    list_filter = (
        'source',
    )

    readonly_fields = (
        'created_at',
    )

    fields = (
        'source',
        'title',
        'title_translation',
        'company',
        'city',
        'date',
        'link',
        'created_at',
    )