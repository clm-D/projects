from django.conf.urls import url

from resgain import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^names/(.+)', views.names, name='names'),
    url(r'^info/(.+)', views.info, name='info'),
]
