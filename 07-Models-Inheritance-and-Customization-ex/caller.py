import os


import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Student, CreditCard, Hotel, Room, SpecialReservation
from datetime import date
# Create queries within functions
# Create a Hotel instance
hotel = Hotel.objects.create(name="Hotel ABC", address="123 Main St")

# Create Room instances associated with the hotel
room1 = Room.objects.create(
    hotel=hotel,
    number="102",
    capacity=2,
    total_guests=1,
    price_per_night=100.00
)

# Create SpecialReservation instance
special_reservation1 = SpecialReservation(
    room=room1,
    start_date=date(2023, 1, 1),
    end_date=date(2023, 1, 5)
)

