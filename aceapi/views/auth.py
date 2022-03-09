from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from aceapi.models import AppUser
from aceapi.models.day import Day


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of an app_user

    Method arguments:
      request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=username, password=password)

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key,
            'user_id': authenticated_user.id
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''
    if request.data['tutor']:
        # Create a new user by invoking the `create_user` helper method
        # on Django's built-in User model
        new_user = User.objects.create_user(
            username=request.data['username'],
            password=request.data['password'],
            first_name=request.data['firstName'],
            last_name=request.data['lastName'],
            email=request.data['email'],
            is_staff = 1
        )

        # Now save the extra info in the aceapi_appUser table
        # Depending on if a student or a tutor are being registered,
        # certain fields will be left as null

        app_user = AppUser.objects.create(
            user=new_user,
            bio=request.data['bio'],
            billing_rate = request.data['billingRate']

        )


        # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=app_user.user)
        # Return the token to the client
        data = {
                'token': token.key,
                'user_id': app_user.id
            }
        return Response(data)

    else:
        # Create a new user by invoking the `create_user` helper method
        # on Django's built-in User model
        new_user = User.objects.create_user(
            username=request.data['username'],
            password=request.data['password'],
            first_name=request.data['firstName'],
            last_name=request.data['lastName'],
            email=request.data['email']
        )

        app_user = AppUser.objects.create(
            user=new_user,
            bio=request.data['bio'],
            day = Day.objects.get(pk=request.data['dayId']),
            start_time = request.data['startTime'],
            end_time = request.data['endTime'],
            parent_name = request.data['parentName'],
            parent_email = request.data['parentEmail'],
        )

        # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=app_user.user)
        # Return the token to the client
        data = {
                'token': token.key,
                'user_id': app_user.id
            }
        return Response(data)
