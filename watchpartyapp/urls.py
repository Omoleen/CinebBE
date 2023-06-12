from django.urls import path
from .views import GroupParty

urlpatterns = [
    path('group/<str:pk>/', GroupParty.as_view())
]