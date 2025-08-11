from django.urls import path
from .views import RegisterAPIView, ActivateAPIView, LoginAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('activate/<str:uid>/<str:token>/', ActivateAPIView.as_view(), name='activate'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
