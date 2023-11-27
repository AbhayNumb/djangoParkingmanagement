from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Parking
from django.contrib.auth.decorators import login_required
from datetime import  time


@method_decorator(csrf_exempt, name='dispatch')
class ReserveParkingView(View):
    @method_decorator(login_required)
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))

        try:
            # Function to convert time in HH:MM format to minutes
            def convert_to_minutes(time_str):
                if isinstance(time_str, time):
                    return time_str.hour * 60 + time_str.minute
                hours, minutes = map(int, time_str.split(':'))
                return hours * 60 + minutes

            # Convert from_time and to_time to minutes
            from_time_minutes = convert_to_minutes(data['from_time'])
            to_time_minutes = convert_to_minutes(data['to_time'])

            # Check for overlapping reservations
            overlapping_reservations = Parking.objects.filter(
                parkingid=data['parkingid']
            )

            # Check for overlapping reservations manually
            for reservation in overlapping_reservations:
                reservation_from_minutes = convert_to_minutes(
                    reservation.from_time)
                reservation_to_minutes = convert_to_minutes(
                    reservation.to_time)

                if (
                    (from_time_minutes <= reservation_to_minutes and from_time_minutes >= reservation_from_minutes) or
                    (to_time_minutes <= reservation_to_minutes and to_time_minutes >=
                     reservation_from_minutes)
                ):
                    return JsonResponse({'message': 'Overlapping reservations are not allowed'}, status=400)

            # If no overlap, create the reservation
            parking = Parking.objects.create(
                parkingid=data['parkingid'],
                from_time=data['from_time'],
                to_time=data['to_time'],
                user=request.user,
            )
            return JsonResponse({'message': 'Parking reservation created successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class GetAllBookingsView(View):
    def get(self, request):
        bookings = Parking.objects.all()
        booking_list = []

        for booking in bookings:
            booking_list.append({
                'parkingid': booking.parkingid,
                'from_time': booking.from_time.strftime('%H:%M'),
                'to_time': booking.to_time.strftime('%H:%M'),
                'user': booking.user.username,
            })

        return JsonResponse({'bookings': booking_list}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class GetAllPaymentView(View):
    price = 5

    def get(self, request):
        booking_list = []
        total_payment=0
        user = request.user  # Assuming the user is authenticated
        bookings = Parking.objects.filter(user=user)
        for booking in bookings:
            hrdiff = (booking.to_time.hour-booking.from_time.hour)*60
            mindiff = booking.to_time.minute-booking.from_time.minute
            cost = (hrdiff+mindiff)*self.price
            booking_list.append({
                'parkingid': booking.parkingid,
                'from_time': booking.from_time,
                'to_time': booking.to_time,
                'user': booking.user.username,
                'total_price': cost,
            })
            total_payment += cost
        return JsonResponse({'bookings': booking_list, 'total_payment': total_payment}, status=200)


# username,parkingid,from,to
@method_decorator(csrf_exempt, name='dispatch')
class SignupView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))

        try:
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            return JsonResponse({'message': 'User created successfully'}, status=200)
        except IntegrityError:
            return JsonResponse({'message': 'Email or username already exists'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        user = authenticate(
            request, username=data['username'], password=data['password'])

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid username or password'}, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=200)
