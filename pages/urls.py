from django.urls import path

from .views import *

urlpatterns = [
    path('', init, name='init'),
    path('search', search, name='search'),
    path('newAccount', newAccount, name='newAccount'),
    path('createUser', createUser, name='createUser'),
    path('homePage/admin', adminPage, name='admin'), # #5.3 comment out this line
    path('homePage/<str:username>', homePage, name='homePage'),
    path('pages/<str:name>', page, name='page'),
    path('pages/<str:name>/delete', deletePage, name='delete')
]
