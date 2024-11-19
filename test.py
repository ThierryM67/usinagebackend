from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode

user_id = 4

uidb64 = urlsafe_base64_encode(force_bytes(user_id))
print(uidb64)

uid = urlsafe_base64_decode(uidb64).decode()
print(uid)