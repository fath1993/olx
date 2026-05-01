from django.db import models


class Settings(models.Model):
    LANGUAGES = (
        ('en', 'en'),
        ('fa', 'fa'),
    )
    scraper_active = models.BooleanField(default=False)
    translated_language = models.CharField(max_length=255, choices=LANGUAGES, default='en', null=False, blank=False, verbose_name='translated language')


class JobLink(models.Model):
    link = models.CharField(max_length=3000, null=False, blank=False, verbose_name='link')


class Job(models.Model):
    JOB_SOURCE = (
        ('olx', 'olx'),
        ('ejobs', 'ejobs'),
    )
    source = models.CharField(max_length=255, choices=JOB_SOURCE, null=False, blank=False, verbose_name='source')
    title = models.CharField(max_length=1000, null=False, blank=False, verbose_name='title')
    title_translation = models.CharField(max_length=1000, null=True, blank=True, verbose_name='title translation')
    company = models.CharField(max_length=1000, null=True, blank=True, verbose_name='company')
    city = models.CharField(max_length=1000, null=True, blank=True, verbose_name='city')
    date = models.CharField(max_length=1000, null=True, blank=True, verbose_name='date')
    link = models.CharField(max_length=3000, null=True, blank=True, verbose_name='link')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')

