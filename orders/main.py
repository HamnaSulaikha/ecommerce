

from django.conf import settings
import razorpay


client = razorpay.Client(auth=(settings.razorpay_key_id, settings.key_secret))
data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }
payment = client.order.create(data=data)