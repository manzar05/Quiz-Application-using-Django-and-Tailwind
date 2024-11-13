from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('landing_register/', RegisterLandingPage.as_view(),name="register-page"),
    path('landing_login/', LoginLandingPage.as_view(),name="login"),
    path('logout/', Logout.as_view(),name="logout"),
    # Templates
    path('', Home.as_view(),name="home"),
    path('test/', TestPage.as_view(),name="test_page"),
    # API's
    path('clear_previous_response/', ClearResponse.as_view(),name="clear_previous_response"),
    path('start_test/', StartTest.as_view(),name="start_test"),
    path('get_result/', ResultView.as_view(),name="get_result"),
]
