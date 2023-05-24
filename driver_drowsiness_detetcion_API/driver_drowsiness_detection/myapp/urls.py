from django.urls import path, include
from .views import DriverAPIView
urlpatterns = [
    path('', DriverAPIView.as_view(), name='drowsiness_detection'),
]