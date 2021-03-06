from rest_framework import serializers

from django.contrib.auth.models import User
from alkilab.apps.reservations.models import Room, Person, ReservationState, \
                                             Country, State, City, \
                                             RoomType, RoomState, Room, \
                                             Reservation, Rental


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
    
    def validate(self, data):
        user = User.objects.filter(username = data['username'])
        email = User.objects.filter(email = data['email'])

        if user:
            raise serializers.ValidationError("The user already exists")
        
        if email:
            raise serializers.ValidationError("The email already exists")

        return data

class PersonSerializer(serializers.ModelSerializer):

    user = UserSerializer

    class Meta:
        model = Person
        fields = ('id', 'firstname', 'lastname','user')

    # def validate(self, data):
    #     return data
        # user_data = data.pop('user')
        # serializer = UserSerializer(data=user_data)

        # if not serializer.is_valid():
        #     raise serializer.errors

        # return data

    # def create(self, validated_data):
    #     user_created = self.user.save()
    
    #     person_data = {'firstname': validated_data.data['firstname'],
    #                    'lastname': validated_data.data['lastname'],
    #                    'user': user_created}

    #     person_serializer = PersonSerializer(data = person_data)

class ReservationStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationState
        fields = ('id', 'name')

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name')


class StateSerializer(serializers.ModelSerializer):

    country = CountrySerializer

    class Meta:
        model = State
        fields = ('id', 'name', 'country')

class CitySerializer(serializers.ModelSerializer):
    
    state = StateSerializer

    class Meta:
        model = City
        fields = ('id', 'name', 'state')

class RoomTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RoomType
        fields = ('id', 'name')

class RoomStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomState
        fields = ('id', 'name')

class RoomSerializer(serializers.ModelSerializer):

    city = CitySerializer
    room_state = RoomStateSerializer
    room_type = RoomTypeSerializer

    class Meta:
        model = Room
        fields = ('id', 'name', 'address', 'capacity',
                  'enabled', 'use_counter', 'city',
                  'room_state', 'room_type')

class ReservationSerializer(serializers.ModelSerializer):

    person = PersonSerializer
    room = RoomSerializer
    state = StateSerializer

    class Meta:
        model = Reservation
        fields = ('id', 'date', 'start_hour',
                  'end_hour', 'purpose', 'est_attendance',
                  'person', 'room', 'state')

class RentalSerializer(serializers.ModelSerializer):

    reservation = ReservationSerializer

    class Meta:
        model = Rental
        fields = ('id', 'attendance', 'reservation')        