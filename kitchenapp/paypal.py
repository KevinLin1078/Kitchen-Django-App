from django.contrib import messages
from django.conf import settings

from paypal.standard.forms import PayPalPaymentsForm

from django.urls import reverse

def process_payment(request):
#     order_id = request.session.get('order_id')
#     order = get_object_or_404(Order, id=order_id)
    host = request.get_host()
 
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': 2.34 ,
        'item_name': 'Order {}'.format(19),
        'invoice': str('19'),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }
 
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'forms.html', {'order': 119, 'form': form})

