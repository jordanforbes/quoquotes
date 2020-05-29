from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index),
    path('success', views.success),
    path('register', views.register),
    path('quotes', views.quotelist),
    path('users/<user_id>', views.usershow),
    path('quotes/<quote_id>', views.quoteedit),
    path('quotes/<quote_id>/update', views.quoteupdate),
    path('quotes/<quote_id>/delete', views.deleteQuote),
    path('addquote', views.addQuote),
    path('login', views.login),
    path('logout', views.logout)
]
