from django.urls import path
from .views import *

app_name = 'systemmanagement'

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('passwordrecovery/', PasswordRecoveryView.as_view()),
    path('passwordrecoverysuccess/', PasswordRecoverySuccessView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('browseusers/', BrowseUsersView.as_view())
]
