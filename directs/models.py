from django.db import models
from client.models import Client
from manufacturer.models import Manufacturer
from django.db.models import Max
  

#Messages from client to manufacturer
class ClientMessage(models.Model):
    client_user = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client_user_cmsg", null=True, blank=True)
    manufacturer_user = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="manufacturer_user_cmsg", null=True, blank=True)
    sender = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="from_user")
    receiver = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="to_user")
    body = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def send(from_user, to_user, body):
        send_client_message = ClientMessage(
            client_user = from_user,
            sender = from_user,
            receiver = to_user,
            body = body,
            read = True
            )
        send_client_message.save()

        receive_client_message = ClientMessage(
            manufacturer_user = to_user,
            sender = from_user,
            receiver = to_user,
            body = body,
            read = False
        )
        receive_client_message.save()

        return send_client_message
    
    def get_message( user):
        client_messages = []

        messages = ClientMessage.objects.filter(manufacturer_user=user, read=False).annotate(last=Max('created')).order_by('-last')
        '''
        for message in messages:
            client_messages.append({
                'client_sender': Client.objects.get(first_name = message['sender']['first_name']),
                'last': message['last'],
                'unread': ClientMessage.objects.filter(manufacturer_user=user, sender=message['sender'], read=False).count(),
                'body': ClientMessage.objects.filter(manufacturer_user=user, sender=message['sender'], read=False).values('body')
            })
        '''

        return messages
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.body
        
    

#Messages from manufacturer to client
class ManufacturerMessage(models.Model):
    client_user = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client_user_mmsg", null=True, blank=True)
    manufacturer_user = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="manufacturer_user_mmsg", null=True, blank=True)
    sender = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="from_user")
    receiver = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="to_user")
    body = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def send(from_user, to_user, body):
        send_manufacturer_message = ManufacturerMessage(
            manufacturer_user = from_user,
            sender = from_user,
            receiver = to_user,
            body = body,
            read = True
            )
        send_manufacturer_message.save()

        receive_manufacturer_message = ManufacturerMessage(
            client_user = to_user,
            sender = from_user,
            receiver = to_user,
            body = body,
            read = False
        )
        receive_manufacturer_message.save()

        return send_manufacturer_message
    
    def get_message(user):
        manufacturer_messages = []

        messages = ManufacturerMessage.objects.filter(client_user=user, read=False).annotate(last=Max('created')).order_by('-last')
        '''
        for message in messages:
            manuf_sender_id = message.sender
            manuf_sender = Manufacturer.objects.filter(id=manuf_sender_id).values('first_name')
            manufacturer_messages.append({
                #'manufacturer_sender': Manufacturer.objects.get(first_name = message['sender']['first_name']),
                'manufacturer_sender': manuf_sender,
                'last': message['last'],
                'unread': ManufacturerMessage.objects.filter(client_user=user, sender=message['sender'], read=False).count(),
                'body': ManufacturerMessage.objects.filter(client_user=user, sender=message['sender'], read=False).values('body')
            })
        '''

        return messages
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.body
        