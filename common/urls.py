from django.urls import path, include, re_path
from common.api.user import Register, ValidateOTP, ValidateMobileOTP, LoginOTP, LoginApiView


app_name = "common"

urlpatterns = [
    # path('sendotp/', SendPhoneOTP.as_view()),
    # path('validatemobileotp/', ValidateMobileOTP.as_view()),
    path('validateotp/', ValidateOTP.as_view()),
    path('register/', Register.as_view()),
    path('login/', LoginApiView.as_view()),
    path('login-otp/', LoginOTP.as_view()),

	# path('' , login_attempt , name="login"),
    # path('register' , register , name="register"),
    # path('otp' , otp , name="otp"),
    # path('login-otp', login_otp , name="login_otp")

]