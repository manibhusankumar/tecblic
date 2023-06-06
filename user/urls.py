from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.UsersList.as_view(), name='list'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', views.VerifyView.as_view(), name='token_verify'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('forgot_password/', views.ForgotPassword.as_view(), name='change_password'),
    path('forgot_password/verfy_otp', views.VerifyOTPforgotpasswordView.as_view(), name='verify_otp'),

]