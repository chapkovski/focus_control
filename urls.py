from django.conf.urls import url
from otree.default_urls import urlpatterns
from trust import focus
# from . import views
print('SUKA')
urlpatterns.append(url(r'^trust/export/$', focus.focustable))
