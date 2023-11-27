from django.urls import path
from .views import SignupView, LoginView, LogoutView,GetAllBookingsView,ReserveParkingView,GetAllPaymentView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('getallbooking/', GetAllBookingsView.as_view(), name='getallbookingsview'),
    path('getallpayment/', GetAllPaymentView.as_view(), name='getallpaymentview'),
    path('reserve-parking/', ReserveParkingView.as_view(), name='reserveparkingview'),
]