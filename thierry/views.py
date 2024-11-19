from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail

from rest_framework.decorators import api_view
from .serializers import CustomPasswordResetConfirmSerializer, ContactSerializer
from .serializers import NewsSerializer, ClientFAQSerializer, ManFAQSerializer, PasswordResetSerializer, AdminSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import jwt
from .models import News, ManFAQ, ClientFAQ,Contact, Admin
from datetime import timedelta, datetime, timezone


frontEndURL = 'http://localhost:3000'

#User views

@api_view(['POST'])
def thierryRegister(request):
    serializer = AdminSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


@api_view(['PUT'])
def adminUpdate(request, pk):
    admin = Admin.objects.get(id=pk)
    serializer = AdminSerializer(instance=admin, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def thierryLogin(request):
    email = request.data['email']
    password1 = request.data['password1']

    user = Admin.objects.filter(email=email).first()

    if user is None:
        raise AuthenticationFailed('user not found!')
    
    if user.password1 != password1:
        raise AuthenticationFailed('Incorrect password!')

    #if not client.check_password(password):
    #    raise AuthenticationFailed('Incorrect password!')

    payload = {
        'id': user.id,
        'exp': datetime.now(timezone.utc) + timedelta(days=2),
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


@api_view(['GET'])
def thierryDetail(request):
    token = request.COOKIES.get('jwt')
    #token = request.headers.get('Authorization')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    admin = Admin.objects.filter(id=payload['id']).first()
    serializer = AdminSerializer(admin)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
def thierryUpdate(request, pk):
    admin = Admin.objects.get(id=pk)
    serializer = AdminSerializer(instance=admin, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def thierryDelete(request):

    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    user = request.user  # Get the authenticated user
    user.delete()  # Delete the user instance

    return Response({"detail": "User account has been deleted."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def passwordReset(request):
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        user = Admin.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = user.pk

        reset_url = f"{frontEndURL}/adresetconfirm/{uid}/{token}/"

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
        # uid = urlsafe_base64_decode(uidb64).decode()
        uid = kwargs.get('uid')
        user = Admin.objects.get(pk=uid)
    except (Admin.DoesNotExist, ValueError, TypeError, OverflowError):
        return Response({"detail": "Invalid user or UID."})

    # Check the token validity
    if not default_token_generator.check_token(user, token):
        return Response({"detail": "Invalid or expired token."})
    
    serializer = CustomPasswordResetConfirmSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"detail": "Password has been reset."})
    return Response(serializer.errors)





#News views

@api_view(['POST'])
def newsCreate(request):
    serializer = NewsSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


#All general requests
@api_view(['GET'])
def newsList(request):
    news = News.objects.all()
    serializer = NewsSerializer(news, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def newsDetail(request, pk):
    news = News.objects.get(id=pk)
    serializer = NewsSerializer(news, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def newsUpdate(request, pk):
    news = News.objects.get(id=pk)
    serializer = NewsSerializer(instance=news, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def newsDelete(request, pk):
    news = News.objects.get(id=pk)
    news.delete()

    return Response('News article successfully deleted')




#FAQ views

@api_view(['POST'])
def ManFAQCreate(request):
    serializer = ManFAQSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


#All FAQs
@api_view(['GET'])
def ManFAQList(request):
    faq = ManFAQ.objects.all()
    serializer = ManFAQSerializer(faq, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def ManFAQDetail(request, pk):
    faq = ManFAQ.objects.get(id=pk)
    serializer = ManFAQSerializer(faq, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def ManFAQUpdate(request, pk):
    faq = ManFAQ.objects.get(id=pk)
    serializer = ManFAQSerializer(instance=faq, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def ManFAQDelete(request, pk):
    faq = ManFAQ.objects.get(id=pk)
    faq.delete()

    return Response('FAQ successfully deleted')



@api_view(['POST'])
def ClientFAQCreate(request):
    serializer = ClientFAQSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


#All clients Faqa
@api_view(['GET'])
def ClientFAQList(request):
    faq = ClientFAQ.objects.all()
    serializer = ClientFAQSerializer(faq, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def ClientFAQDetail(request, pk):
    faq = ClientFAQ.objects.get(id=pk)
    serializer = ClientFAQSerializer(faq, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def ClientFAQUpdate(request, pk):
    faq = ClientFAQ.objects.get(id=pk)
    serializer = ClientFAQSerializer(instance=faq, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def ClientFAQDelete(request, pk):
    faq = ClientFAQ.objects.get(id=pk)
    faq.delete()

    return Response('FAQ successfully deleted')




#COntact views

@api_view(['POST'])
def contactCreate(request):
    serializer = ContactSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


#All general requests
@api_view(['GET'])
def contactList(request):
    contacts = Contact.objects.all()
    serializer = ContactSerializer(contacts, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def contactDetail(request, pk):
    contact = Contact.objects.get(id=pk)
    serializer = ContactSerializer(contact, many=False)
    return Response(serializer.data)