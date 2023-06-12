from .views import Register, ForgotPassword, VerifyToken, Change
from django.urls import path

urlpatterns = [
    path('register/', Register.as_view()),
    path('forgot/', ForgotPassword.as_view()),
    path('verify/', VerifyToken.as_view()),
    path('check/', Change.as_view()),
]