"""web_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from baby_bed import views as baby_bed_views
from baby_bed import server as baby_bed_server

urlpatterns = [
    url(r'^$', baby_bed_views.index),
    url(r'^bed-wetting', baby_bed_server.bed_wetting, name='bed-wetting'),
    url(r'^temp', baby_bed_server.temp, name='temp'),
    url(r'^inBed', baby_bed_server.inBed, name='inbed'),
    url(r'^sleepTime', baby_bed_server.sleepTime, name='sleeptime'),
    url(r'^isCry', baby_bed_server.isCry, name='isCry'),
    url(r'^isSleeping', baby_bed_server.isSleeping, name='isSleeping'),
    url(r'^history/$', baby_bed_server.history, name='history'),
]
