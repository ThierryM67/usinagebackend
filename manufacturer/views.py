from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from client.models import Request2
from client.serializers import RequestSerializer2
from .serializers import CustomPasswordResetConfirmSerializer, PasswordResetSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import ManufacturerSerializer, OfferSerializer, RatingSerializer
from .models import Manufacturer, Offer, Rating
from datetime import datetime,timedelta, timezone
import jwt
from django.forms.models import model_to_dict

frontEndURL = 'http://localhost:3000'


#Manufacturer Views
@api_view(['POST'])
def manufacturerRegister(request):
    serializer = ManufacturerSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def manufacturerLogin(request):
    email = request.data['email']
    password1 = request.data['password1']

    manufacturer = Manufacturer.objects.filter(email=email).first()

    if manufacturer is None:
        raise AuthenticationFailed('Manufacturer not found!')
    
    if manufacturer.password1 != password1:
        raise AuthenticationFailed('Incorrect password!')

    # if not manufacturer.check_password(password):
    #     raise AuthenticationFailed('Incorrect password!')

    payload = {
        'email': manufacturer.email,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=60),
        'iat': datetime.now(timezone.utc)
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')

    response = Response()

    response.set_cookie(key='jwt', value=token, httponly=True)
    response['Authorization'] = token
    response.data = {
        'jwt': token
    }
    return response


@api_view(['POST'])
def passwordReset(request):
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        user = Manufacturer.objects.get(email=email)
        #uid = urlsafe_base64_encode(force_bytes(user.pk))
        uid = user.pk
        token = default_token_generator.make_token(user)

        # Construct the password reset URL
        current_site = get_current_site(request)
        #reset_url = f"http://{current_site.domain}{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"
        #reset_url = f"http://{current_site.domain}/manufacturer/password-reset-confirm/{uid}/{token}/"
        reset_url = f"{frontEndURL}/ResetConfirm/{uid}/{token}/"

        # Send the email
        send_mail(
            "Password Reset Request",
            f"Click the link to reset your password: {reset_url}",
            "noreply@monusinage.com",
            [email],
        )
        return Response({"message": "Password reset link sent"})

    return Response(serializer.errors)


@api_view(['POST'])
def passwordResetConfirm(request, *args, **kwargs):

    uidb64 = kwargs.get('uidb64')
    token = kwargs.get('token')

    try:
        # Decode the uidb64 to get the user ID
        #uid = urlsafe_base64_decode(uidb64).decode()
        uid = kwargs.get('uid')
        user = Manufacturer.objects.get(pk=uid)
    except (Manufacturer.DoesNotExist, ValueError, TypeError, OverflowError):
        return Response({"detail": "Invalid user or UID."})

    # Check the token validity
    if not default_token_generator.check_token(user, token):
        return Response({"detail": "Invalid or expired token."})
    
    serializer = CustomPasswordResetConfirmSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"detail": "Password has been reset."})
    return Response(serializer.errors)


@api_view(['GET'])
def manufacturerDetail(request):
    #token = request.COOKIES.get('jwt')
    token = request.headers.get('Authorization')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    manufacturer = Manufacturer.objects.filter(email=payload['email']).first()
    if manufacturer is None:
        raise AuthenticationFailed('Manufacturer not found!')
    serializer = ManufacturerSerializer(manufacturer)
    return Response(serializer.data)


@api_view(['GET'])
def manufacturerDetail2(request, pk):
    manufacturer = Manufacturer.objects.filter(id=pk).first()
    serializer = ManufacturerSerializer(manufacturer)
    return Response(serializer.data)


@api_view(['GET'])
def manufacturers(request):
    manufacturers = Manufacturer.objects.all()
    serializer = ManufacturerSerializer(manufacturers, many=True)

    return Response(serializer.data)


@api_view(['PUT'])
def manufacturerUpdate(request, pk):
    manufacturer = Manufacturer.objects.get(id=pk)
    serializer = ManufacturerSerializer(instance=manufacturer, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def manufacturerLogout(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'successfully logged out'
    }
    return response


@api_view(['DELETE'])
def manufacturerDelete(request, pk):
    manufacturer = Manufacturer.objects.get(id=pk)
    manufacturer.delete()

    return Response('Manufacturer successfully deleted')





#Offer views
@api_view(['POST'])
def offerCreate(request, pk):
    serializer = OfferSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)

@api_view(['POST'])
def offerCreateb(request):

    offerObj = Offer(
        request = Request2.objects.get(title=request.data['request']),
        manufacturer = Manufacturer.objects.get(first_name=request.data['manufacturer']),
        price = request.data['price'],
        days = request.data['days'],
        description = request.data['description']
    )

    serializer = OfferSerializer(data=model_to_dict(offerObj))

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


#All general offers
@api_view(['GET'])
def generalOfferList(request):
    offers = Offer.objects.all()
    serializer = OfferSerializer(offers, many=True)
    return Response(serializer.data)


#All offers per manufacturer
@api_view(['GET'])
def manufacturerOfferList(request, pk):
    manufacturer = Manufacturer.objects.get(id = pk)
    manufacturer_offers = Offer.objects.filter( manufacturer = manufacturer)
    serializer = OfferSerializer(manufacturer_offers, many=True)
    return Response(serializer.data)

#All offers per request
@api_view(['GET'])
def requestOfferList(request, pk):
    prodrequest = Request2.objects.get(id = pk)
    request_offers = Offer.objects.filter( request = prodrequest)
    serializer = OfferSerializer(request_offers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def manufacturerRequestList(request, pk):
    manufacturer = Manufacturer.objects.get(id = pk)
    manufacturer_request = Request2.objects.filter( accepted_manufacturer_id = pk)
    serializer = RequestSerializer2(manufacturer_request, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def offerDetail(request, pk):
    offer = Offer.objects.get(id=pk)
    serializer = OfferSerializer(offer, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def offerManufs(request):
    manuf_id = request.data['manufacturers']
    manufacturers = Manufacturer.objects.filter(id__in=manuf_id)
    serializer = ManufacturerSerializer(manufacturers, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def offerUpdate(request, pk):
    offer = Offer.objects.get(id=pk)
    serializer = OfferSerializer(instance=offer, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def offerDelete(request, pk):
    offer = Offer.objects.get(id=pk)
    offer.delete()

    return Response('Offer successfully deleted')





#Manufacturer Rating views
@api_view(['POST'])
def ratingCreate(request):
    serializer = RatingSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def ratingList(request):
    ratings = Rating.objects.all()
    serializer = RatingSerializer(ratings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ratingDetail(request, pk):
    rating = Rating.objects.get(id=pk)
    serializer = RatingSerializer(rating, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def ratingUpdate(request, pk):
    offer = Offer.objects.get(id=pk)
    rating = Rating.objects.get(offer = offer)
    serializer = RatingSerializer(instance=rating, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


#this view is meant to be used by a manufacturer deleting a rating of a client
@api_view(['DELETE'])
def ratingDelete(request, pk):
    rating = Rating.objects.get(id=pk)
    rating.delete()

    return Response('Rating successfully deleted')


#client average rating
@api_view(['GET'])
def manufacturerAverageRating(request, pk):
    manufacturer = Manufacturer.objects.get(id = pk)
    offers = Offer.objects.filter( manufacturer = manufacturer)
    offer_ratings = Rating.objects.filter(offer__in = offers)
    serializer = RatingSerializer(offer_ratings, many=True)
    ratings_data = serializer.data

    sum = 0
    for rating in ratings_data:
        sum += int(rating['rating_value'])

    avg_rating = sum/len(ratings_data) 
    return Response(avg_rating)

'''
#login required decorator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_api_view(request):
    return Response({"message": "Hello, authenticated user!"})
'''