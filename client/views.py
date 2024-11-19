from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import ClientSerializer,RequestSerializer,RatingSerializer, RequestSerializer2
from .serializers import CustomPasswordResetConfirmSerializer,NewsSerializer, PasswordResetSerializer
from .models import Client, Request, Rating, News, Request2
from datetime import datetime,timedelta, timezone
import jwt
from django.forms.models import model_to_dict


# from rest_framework import status
# from paypalrestsdk import Payment
# from .serializers import OrderRequestSerializer, CartItemSerializer
from paypalrestsdk import notifications
from django.http import HttpResponse, HttpResponseBadRequest





frontEndURL = 'http://localhost:3000'


#Client Views
@api_view(['POST'])
def clientRegister(request):
    serializer = ClientSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def clientLogin(request):
    email = request.data['email']
    password1 = request.data['password1']

    client = Client.objects.filter(email=email).first()

    if client is None:
        raise AuthenticationFailed('Client not found!')
    
    if client.password1 != password1:
        raise AuthenticationFailed('Incorrect password!')

    #if not client.check_password(password):
    #    raise AuthenticationFailed('Incorrect password!')

    payload = {
        'email': client.email,
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
        user = Client.objects.get(email=email)
        #uid = urlsafe_base64_encode(force_bytes(user.pk))
        uid=user.pk
        token = default_token_generator.make_token(user)

        # Construct the password reset URL
        current_site = get_current_site(request)
        #reset_url = f"http://{current_site.domain}{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"
        #reset_url = f"http://{current_site.domain}/client/password-reset-confirm/{uid}/{token}/"
        reset_url = f"{frontEndURL}/cresetconfirm/{uid}/{token}/"

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

    #uidb64 = kwargs.get('uidb64')
    token = kwargs.get('token')

    try:
        # Decode the uidb64 to get the user ID
        #uid = urlsafe_base64_decode(uidb64).decode()
        uid = kwargs.get('uid')
        user = Client.objects.get(pk=uid)
    except (Client.DoesNotExist, ValueError, TypeError, OverflowError):
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
def clientDetail(request):
    #token = request.COOKIES.get('jwt')
    token = request.headers.get('Authorization')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    client = Client.objects.filter(email=payload['email']).first()
    if client is None:
        raise AuthenticationFailed('Client not found!')
    serializer = ClientSerializer(client)
    return Response(serializer.data)

@api_view(['GET'])
def clientDetail2(request, pk):

    client = Client.objects.filter(id=pk).first()
    serializer = ClientSerializer(client)
    return Response(serializer.data)

@api_view(['GET'])
def clients(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)

    return Response(serializer.data)

@api_view(['PUT'])
def clientUpdate(request, pk):
    client = Client.objects.get(id=pk)
    serializer = ClientSerializer(instance=client, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def clientLogout(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'successfully logged out'
    }
    return response


@api_view(['DELETE'])
def clientDelete(request, pk):
    client = Client.objects.get(id=pk)
    client.delete()

    return Response('Client successfully deleted')





#Request views
@api_view(['POST'])
def requestCreate(request):
    serializer = RequestSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def requestCreate2(request):
    serializer = RequestSerializer2(data=request.data)

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)

@api_view(['POST'])
def requestCreateb(request):
    str_to_bool = lambda x: x.lower() == "true" if isinstance(x, str) else False

    # Shallow copy of request data for easy manipulation
    form_data = dict(request.data)
    file_data = dict(request.FILES)

    # Unwrap single-item lists
    for key, value in form_data.items():
        if isinstance(value, list) and len(value) == 1:
            form_data[key] = value[0]

    for key, value in file_data.items():
        if isinstance(value, list) and len(value) == 1:
            file_data[key] = value[0]

    # Process additional fields
    form_data['urgent'] = str_to_bool(form_data.get('urgent'))
    form_data['quantity'] = int(form_data.get('quantity', 1))
    form_data['mailbox_send'] = str_to_bool(form_data.get('mailbox_send'))
    form_data['relaypoint_send'] = str_to_bool(form_data.get('relaypoint_send'))

    # Retrieve client by first name if necessary and set the client ID
    if 'client' in form_data:
        try:
            client = Client.objects.get(first_name=form_data['client'])
            form_data['client'] = client.id
        except Client.DoesNotExist:
            return Response({"error": "Client not found."}, status=400)

    # Combine form_data and request.FILES for the serializer
    #combined_data = {**form_data, **request.FILES}
    combined_data = {**form_data, **file_data}
    print(combined_data)

    # Initialize serializer with combined data
    serializer = RequestSerializer2(data=combined_data)

    # Validate and save if valid
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)

    # Return errors if any
    return Response(serializer.errors, status=400)


#All general requests
@api_view(['GET'])
def generalRequestList(request):
    prod_requests = Request.objects.all()
    serializer = RequestSerializer(prod_requests, many=True)
    return Response(serializer.data)


#All general requests
@api_view(['GET'])
def generalRequestList2(request):
    prod_requests = Request2.objects.all()
    serializer = RequestSerializer2(prod_requests, many=True)
    return Response(serializer.data)

#All requests per client
@api_view(['GET'])
def clientRequestList(request, pk):
    client = Client.objects.get(id = pk)
    client_requests = Request.objects.filter( client = client)
    serializer = RequestSerializer(client_requests, many=True)
    return Response(serializer.data)

#All requests per client
@api_view(['GET'])
def clientRequestList2(request, pk):
    client = Client.objects.get(id = pk)
    client_requests = Request2.objects.filter( client = client)
    serializer = RequestSerializer2(client_requests, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def requestDetail(request, pk):
    prod_request = Request.objects.get(id=pk)
    serializer = RequestSerializer(prod_request, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def requestDetail2(request, pk):
    prod_request = Request2.objects.get(id=pk)
    serializer = RequestSerializer2(prod_request, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def requestUpdate(request, pk):
    prod_request = Request.objects.get(id=pk)
    serializer = RequestSerializer(instance=prod_request, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def requestDelete(request, pk):
    prod_request = Request.objects.get(id=pk)
    prod_request.delete()

    return Response('Request successfully deleted')





#Client Rating views
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
    prod_request = Request.objects.get(id=pk)
    rating = Rating.objects.get(request = prod_request)
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
def clientAverageRating(request, pk):
    client = Client.objects.get(id = pk)
    client_requests = Request.objects.filter( client = client)
    request_ratings = Rating.objects.filter(request__in=client_requests)
    serializer = RatingSerializer(request_ratings, many=True)
    ratings_data = serializer.data

    sum = 0
    for rating in ratings_data:
        sum += int(rating['rating_value'])

    avg_rating = sum/len(ratings_data)
    return Response(avg_rating)
    #return Response({sum, len(ratings_data)})
    {
        "title": "XYZ Request",
        "client": 2,
        "material": "concrete",
        "offer_type": "Classic",
        "description": "I wanna sleep now",
        "urgent": "False",
        "quantity": 4,
        "deadline": "2024-10-29"
}





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



'''
#login required decorator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_api_view(request):
    return Response({"message": "Hello, authenticated user!"})





@api_view(['POST'])
def capture_order(request, order_id):
    """
    Capture a PayPal order once the payer has approved it.
    """
    payer_id = request.data.get("payer_id")
    
    if not payer_id:
        return Response({"error": "Payer ID is missing"}, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve the payment from PayPal using the order_id
    payment = Payment.find(order_id)
    
    # Execute the payment
    if payment.execute({"payer_id": payer_id}):
        return Response({"status": "Payment captured successfully!"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": payment.error}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def create_order(request):
    """
    Create a PayPal order based on cart data.
    """
    serializer = OrderRequestSerializer(data=request.data)
    
    if serializer.is_valid():
        cart = serializer.validated_data["cart"]
        total_amount = 100.00  # You can calculate this from the cart

        # Create PayPal payment object
        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": str(total_amount),
                    "currency": "USD"
                },
                "description": "Sample payment description"
            }],
            "redirect_urls": {
                "return_url": "http://localhost:8000/client/paypal/capture-order/, kwargs={'uidb64': uid, 'token': token}",
                "cancel_url": "http://localhost:8000/client/paypal/cancel/"
            }
        })

        # Create the payment on PayPal
        if payment.create():
            # Find the approval URL from the payment links
            approval_url = next(link.href for link in payment.links if link.rel == "approval_url")
            return Response({"approval_url": approval_url}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": payment.error}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
from django.conf import settings
import json
@api_view(['POST'])
def Webhook(request):

    if "HTTP_PAYPAL_TRANSMISSION_ID" not in request.META:
        return HttpResponseBadRequest()
    
    auth_algo = request.META["HTTP_PAYPAL_AUTH_ALGO"]
    cert_url = request.META["HTTP_PAYPAL_CERT_URL"]
    transmission_id = request.META["HTTP_PAYPAL_TRANSMISSION_ID"]
    transmission_sig = request.META["HTTP_PAYPAL_TRANSMISSION_SIG"]
    transmission_time = request.META["HTTP_PAYPAL_TRANSMISSION_TIME"]
    webhook_id = settings.PAYPAL_WEBHOOK_ID
    event_body = request.body.decode(request.encoding or "utf-8")

    valid = notifications.WebhookEvent.verify(
        transmission_id=transmission_id,
        timestamp=transmission_time,
        webhook_id=webhook_id,
        event_body=event_body,
        cert_url=cert_url,
        actual_sig=transmission_sig,
        auth_algo=auth_algo
    )

    if not valid:
        return HttpResponseBadRequest()
    
    webhook_event = json.loads(event_body)
    event_type = webhook_event["event_type"]

    CHECKOUT_ORDER_APPROVED = "CHECKOUT.ORDER.APPROVED"

    if event_type == CHECKOUT_ORDER_APPROVED:
        customer_email = webhook_event["resource"]["payer"]["email_address"]
        product_link = "https:://monusinage.com"
        send_mail(
            subject="Your access",
            message=f"Thank you for purchasing my product.Here is the link: {product_link}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[customer_email]
        )
        print(customer_email)

    return HttpResponse()
