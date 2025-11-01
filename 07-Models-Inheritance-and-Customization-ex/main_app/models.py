from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet


# Create your models here.

class BaseCharacter(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    class Meta:
        abstract = True


class Mage(BaseCharacter):
    elemental_power = models.CharField(max_length=100)
    spellbook_type = models.CharField(max_length=100)

class Assassin(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    assassination_technique = models.CharField(max_length=100)

class DemonHunter(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    demon_slaying_ability = models.CharField(max_length=100)

class TimeMage(Mage):
    time_magic_mastery = models.CharField(max_length=100)
    temporal_shift_ability = models.CharField(max_length=100)


class Necromancer(Mage):
    raise_dead_ability = models.CharField(max_length=100)

class ViperAssassin(Assassin):
    venomous_strikes_mastery = models.CharField(max_length=100)
    venomous_bite_ability = models.CharField(max_length=100)


class ShadowbladeAssassin(Assassin):
    shadowstep_ability  = models.CharField(max_length=100)

class VengeanceDemonHunter(DemonHunter):
    vengeance_mastery = models.CharField(max_length=100)
    retribution_ability = models.CharField(max_length=100)


class FelbladeDemonHunter(DemonHunter):
    felblade_ability =  models.CharField(max_length=100)



#2
class UserProfile(models.Model):
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)

class Message(models.Model):
    sender= models.ForeignKey(UserProfile,related_name='sent_messages', on_delete=models.CASCADE)
    receiver= models.ForeignKey(UserProfile,related_name='received_messages', on_delete=models.CASCADE)
    content= models.TextField()
    timestamp= models.DateTimeField(auto_now_add=True) #When a record is created you should save the time of the creation
    is_read = models.BooleanField(default=False)

    def mark_as_read(self) -> None:
        self.is_read=True

    def reply_to_message(self,reply_content: str) -> 'Message':
        new_message = Message(sender=self.receiver, receiver=self.sender, content=reply_content)
        new_message.save()
        return new_message

    def forward_message(self,receiver: UserProfile) -> 'Message':
        new_message = Message(sender=self.receiver, receiver=receiver, content=self.content)
        new_message.save()
        return new_message




#3

class StudentIDField(models.PositiveIntegerField):
    @staticmethod
    def validate_field(value) -> int:
        try:
           return int(value)

        except ValueError:
            raise ValueError("Invalid input for student ID")



    def to_python(self, value) -> int:
        return self.validate_field(value)

    def get_prep_value(self, value) -> int:
        validated_value = self.validate_field(value)
        if validated_value <= 0:
            raise ValidationError("ID cannot be less than or equal to zero")

        return validated_value

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = StudentIDField()

#4
# In the "main_app", the field "MaskedCreditCardField" is a type of character field and returns information about the credit card number.
# It should save the card number in a masked format in the database as a string with only the card's last four digits visible
# in the format: "****-****-****-{last_four_card_digits}"
# •	If a data type other than a string is provided as the card number,
# a ValidationError should be raised with the message: "The card number must be a string".
# •	The card number can consist only of digits, otherwise,
# a ValidationError should be raised with the message: "The card number must contain only digits".
# •	The card number must be exactly 16 digits long, otherwise
# a ValidationError should be raised with the message: "The card number must be exactly 16 characters long".

class MaskedCreditCardField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        super().__init__(*args,**kwargs)
    def to_python(self, value):
        if not isinstance(value, str):
            raise ValidationError("The card number must be a string")
        if not value.isdigit():
            raise ValidationError("The card number must contain only digits")

        if len(value) != 16:
            raise ValidationError("The card number must be exactly 16 characters long")

        return f"****-****-****-{value[-4:]}"

class CreditCard(models.Model):
    card_owner = models.CharField(max_length=100)
    card_number = MaskedCreditCardField()

#5

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

class Room(models.Model):
    hotel = models.ForeignKey(to = Hotel, on_delete=models.CASCADE)
    number = models.CharField(max_length=100,unique=True)
    capacity = models.PositiveIntegerField()
    total_guests = models.PositiveIntegerField()
    price_per_night  = models.DecimalField(decimal_places=2, max_digits=10)

    #Before saving an instance of type room in the database:
    # •	If the total number of guests is greater than the capacity of the room, a ValidationError should be raised with the message - "Total guests are more than the capacity of the room".
    # •	If the room is saved successfully, return the message: "Room {room_number} created successfully".

    def clean(self) -> None:
        if self.total_guests > self.capacity:
            raise  ValidationError("Total guests are more than the capacity of the room")

    def save(self,*args,**kwargs) -> str:
        self.clean()
        super().save(*args,**kwargs)

        return f"Room {self.number} created successfully"

class BaseReservation(models.Model):
    class Meta:
        abstract = True
    reservation_type =None
    room = models.ForeignKey(to = Room, on_delete=models.CASCADE)
    start_date= models.DateTimeField()
    end_date = models.DateTimeField()

    def reservation_period(self) -> int:
        return (self.end_date - self.start_date).days

    def calculate_total_cost(self):
        total_cost = self.reservation_period() * self.room.price_per_night
        return round(total_cost, 2)

    def get_overlapping_reservations(self,start_date:date,end_date:date) -> QuerySet['BaseReservation']:
        return self.__class__.objects.filter(
                room=self.room,
                end_date__gte=start_date,
                start_date__lte=end_date)

    @property
    def is_available(self):
        reservations = self.get_overlapping_reservations(self.start_date,self.end_date)
        return not reservations.exists() #todo

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date cannot be after or in the same end date")
        if not self.is_available:
            raise ValidationError(f"Room {self.room.number} cannot be reserved")

    def save(self,*args,**kwargs) :
        self.clean()
        super().save(*args,**kwargs)
        return f"{self.reservation_type} reservation for room {self.room.number}"
class RegularReservation(BaseReservation):

#     Before saving an instance of type regular reservation in the database, check if the reservation dates are implemented correctly:
# •	If the start date is greater than or equal to the end date, a ValidationError should be raised with the message - "Start date cannot be after or in the same end date".
# •	If the reservation being created overlaps with existing reservations (i.e., it has dates that match other reservations), a ValidationError should be raised with the message - "Room {room_number} cannot be reserved". A conflicting reservation occurs when the date range specified for the new reservation clashes with the dates of reservations that already exist.
# •	If the registration is saved successfully, return the message: "Regular reservation for room {room_number}".
# Please be aware that all types of reservations are intended to span until the end date, including the end date itself.

    reservation_type = 'Regular'
class SpecialReservation(BaseReservation):

# Before saving an instance of type special reservation in the database, check if the reservation dates are implemented correctly:
# •	If the start date is greater than or equal to the end date, a ValidationError should be raised with the message - "Start date cannot be after or in the same end date".
# •	If the reservation being created overlaps with existing reservations (i.e., it has dates that match other reservations), a "ValidationError" should be raised with the message - "Room {room_number} cannot be reserved". A conflicting reservation occurs when the date range specified for the new reservation clashes with the dates of reservations that already exist.
# •	If the registration is saved successfully, return the message: "Special reservation for room {room_number}".
# Please be aware that all types of reservations are intended to span until the end date, including the end date itself.
# extend_reservation(days: int) extends existing reservations with the given days.
# •	You should extend an already existing reservation. If the room is not reserved or you try to extend the
# reservation period and the room has been already reserved for the desired period, a ValidationError should be raised with the message
# - "Error during extending reservation".
# •	If the extending is successful, you should return the message: "Extended reservation for room {room_number} with {days} days".
    def extend_reservation(self, days: int) -> str:
        reservation_type = 'Special'
        new_end_date = self.end_date + timedelta(days=days)
        reservations = self.get_overlapping_reservations(self.start_date, self.end_date)
        if reservations:
            raise ValidationError(f"Error during extending reservation")

        self.end_date = new_end_date
        self.save()
        return f"Extended reservation for room {self.room.number} with {days} days"



