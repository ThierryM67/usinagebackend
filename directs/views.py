from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ManufacturerMessage, ClientMessage, Client, Manufacturer
from .serializers import ManufacturerMessageSerializer, ClientMessageSerializer
from django.db.models import Max

# Create your views here.
# @api_view(['GET'])
# def clientUnread(request):
#     messages = ManufacturerMessage.get_message(user=request.user)

#     serializer = ManufacturerMessageSerializer(messages, many=True)

#     return Response(serializer.data)

@api_view(['POST'])
def clientUnread(request):
    id = request.data['id']
    client = Client.objects.filter(id=id).first()
    messages = ManufacturerMessage.get_message(user=client)
    serializer = ManufacturerMessageSerializer(messages, many=True)

    return Response(serializer.data)






# @api_view(['GET'])
# def clientInbox(request):
#     #messages = ManufacturerMessage.objects.filter(client_user=request.user, read=True).annotate(last=Max('created')).order_by('-last')
#     messages = ManufacturerMessage.objects.filter(client_user=request.user).annotate(last=Max('created')).order_by('-last')

#     serializer = ManufacturerMessageSerializer(messages, many=True)

#     return Response(serializer.data)

@api_view(['POST'])
def clientInbox(request):
    id = request.data['id']
    client = Client.objects.filter(id=id).first()
    messages = ManufacturerMessage.objects.filter(client_user=client, read=True).annotate(last=Max('created')).order_by('-last')

    serializer = ManufacturerMessageSerializer(messages, many=True)

    return Response(serializer.data)








# @api_view(['GET'])
# def clientChat(request, pk):
#     manufacturer = Manufacturer.objects.get(id = pk)
#     messages = ManufacturerMessage.objects.filter(client_user=request.user, sender=manufacturer).annotate(last=Max('created')).order_by('-last')

#     serializer = ManufacturerMessageSerializer(messages, many=True)

#     return Response(serializer.data)
@api_view(['POST'])
def clientChat(request, pk):
    manufacturer = Manufacturer.objects.get(id = pk)
    id = request.data['id']
    client = Client.objects.filter(id=id).first()
    messages = ManufacturerMessage.objects.filter(client_user=client, sender=manufacturer).annotate(last=Max('created')).order_by('-last')
    # for message in messages:
    #     message.read = True
    #     message.save()
    serializer = ManufacturerMessageSerializer(messages, many=True)

    return Response(serializer.data)



'''
#get user from request
@api_view(['POST'])
def clientSend(request):
    user = request.user.email
    from_user = Client.objects.filter(email= user ).first()
    data = request.data
    manufacturer = data['manufacturer']
    to_user = Manufacturer.objects.filter(email = manufacturer).first()
    body = data['body']
    message = ClientMessage.send(from_user=from_user, to_user=to_user, body=body)

    serializer = ClientMessageSerializer(message)
    return Response(serializer.data)
'''
#getting user from request body
@api_view(['POST'])
def clientSend(request):
    data = request.data
    manufacturer = data['manufacturer']
    to_user = Manufacturer.objects.filter(id = manufacturer).first()
    body = data['body']
    user = data['client_id']
    from_user = Client.objects.filter(id= user ).first()
    message = ClientMessage.send(from_user=from_user, to_user=to_user, body=body)

    serializer = ClientMessageSerializer(message)

    return Response(serializer.data)









#Manufacturer directs views

# @api_view(['GET'])
# def manufacturerUnread(request):
#     messages = ClientMessage.get_message(user=request.user)

#     serializer = ClientMessageSerializer(messages, many=True)

#     return Response(serializer.data)
@api_view(['POST'])
def manufacturerUnread(request):
    id = request.data['id']
    manufacturer = Manufacturer.objects.filter(id=id).first()
    messages = ClientMessage.get_message(user=manufacturer)

    serializer = ClientMessageSerializer(messages, many=True)

    return Response(serializer.data)





# @api_view(['GET'])
# def manufacturerInbox(request):
#     messages = ClientMessage.objects.filter(manufacturer_user=request.user).annotate(last=Max('created')).order_by('-last')
#     #messages = ClientMessage.objects.filter(manufacturer_user=request.user, read=True).annotate(last=Max('created')).order_by('-last')

#     serializer = ClientMessageSerializer(messages, many=True)

#     return Response(serializer.data)
@api_view(['POST'])
def manufacturerInbox(request):
    id = request.data['id']
    manufacturer = Manufacturer.objects.filter(id=id).first()
    messages = ClientMessage.objects.filter(manufacturer_user=manufacturer, read=True).annotate(last=Max('created')).order_by('-last')
    #messages = ClientMessage.objects.filter(manufacturer_user=request.user, read=True).annotate(last=Max('created')).order_by('-last')

    serializer = ClientMessageSerializer(messages, many=True)

    return Response(serializer.data)




# @api_view(['GET'])
# def manufacturerChat(request, pk):
#     client = Client.objects.get(id = pk)
#     messages = ClientMessage.objects.filter(manufacturer_user=request.user, sender=client).annotate(last=Max('created')).order_by('-last')

#     serializer = ClientMessageSerializer(messages, many=True)

#     return Response(serializer.data)
@api_view(['POST'])
def manufacturerChat(request, pk):
    id = request.data['id']
    manufacturer = Manufacturer.objects.filter(id=id).first()
    client = Client.objects.get(id = pk)
    messages = ClientMessage.objects.filter(manufacturer_user=manufacturer, sender=client).annotate(last=Max('created')).order_by('-last')
    # for message in messages:
    #     message.read = True
    #     message.save()
    serializer = ClientMessageSerializer(messages, many=True)

    return Response(serializer.data)





#get chat messages with particular client
'''
#getting user from request
@api_view(['POST'])
def manufSend(request):
    from_user = request.user
    data = request.data
    client = data['client']
    to_user = Client.objects.get(email = client)
    body = data['body']
    message = ManufacturerMessage.send(from_user=from_user, to_user=to_user, body=body)

    serializer = ManufacturerMessageSerializer(message)
    return Response(serializer.data)
'''

#getting user from request body
@api_view(['POST'])
def manufSend(request):
    data = request.data
    client = data['client']
    to_user = Client.objects.filter(id = client).first()
    body = data['body']
    user = data['manufacturer_id']
    from_user = Manufacturer.objects.filter(id= user ).first()
    message = ManufacturerMessage.send(from_user=from_user, to_user=to_user, body=body)

    serializer = ManufacturerMessageSerializer(message)

    return Response(serializer.data)

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