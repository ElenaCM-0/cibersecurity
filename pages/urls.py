from django.urls import path

from .views import *

urlpatterns = [
    path('', init, name='init'),
    path('search', search, name='search'),
    path('createUser', createUser, name='createUser'),
    path('homePage', homePage, name='homePage'),
    path('pages/<str:name>', page, name='page'),
    path('snippet', snippet, name='snippet')
]
