from django.urls import path
from .views import RegisterAPIView, ActivateAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('activate/<str:uid>/<str:token>/', ActivateAPIView.as_view(), name='activate'),
]
