from django.urls import path
from polls import views

urlpatterns = [
    path('content_api/', views.content_api),
    path('account_creation/', views.create_user_api)

]