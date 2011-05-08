from zope import interface
from getpaid.core import interfaces
from getpaid.brownpapertickets.bpt import BrownPaperTicketsClient
from getpaid.brownpapertickets.interfaces import IBPTOptions
from getpaid.brownpapertickets.interfaces import IBPTEventLineItem


class BPTPaymentProcessor(object):
    interface.implements(interfaces.IPaymentProcessor)

    options_interface = IBPTOptions

    def __init__(self, context):
        self.context = context

    def authorize(self, order, payment):
        """Pay for a cart of BPTEventLineItems using the Brown Paper Tickets API.
        
        Each item in the order's shopping cart must provide IBPTEventLineItem,
        and must have its product_code set to the BPT price_id.
        """
        
        options = IBPTOptions(self.context)
        client = BrownPaperTicketsClient()
        
        # Make sure cart only has Brown Paper Tickets items
        for item in order.shopping_cart.values():
            if not IBPTEventLineItem.providedBy(item):
                raise Exception('Cart contains items that are not Brown Paper Tickets events.')

        # BPT checkout occurs in 4 stages:
        # 1. Create cart
        res = client('cart',
            id = options.developer_id,
            stage = 1,
            )
        resultcode = res.find('resultcode').text
        if resultcode != '000000':
            raise Exception('Could not create cart: %s' % res.find('note').text)
        cart_id = res.find('cart_id').text
        
        # 2. Add tickets to cart
        for item in order.shopping_cart.values():
            res = client('cart',
                id = options.developer_id,
                stage = 2,
                cart_id = cart_id,
                price_id = item.product_code,
                quantity = item.quantity,
                shipping = '2', # XXX ticketless will-call
                )
            resultcode = res.find('resultcode').text
            if resultcode != '000000':
                raise Exception('Could not add tickets to cart: %s' % res.find('note').text)
        
        # 3. Submit shipping information -- skipping for now,
        #    revisit if we switch away from ticketless will-call above
        
        # 4. Submit billing info
        card_type = payment.credit_card_type
        if card_type == 'MasterCard':
            card_type = 'Mastercard'
        if card_type == 'American Express':
            card_type = 'Amex'
        if options.test_mode:
            card_number = '1234567890000000'
        else:
            card_number = payment.credit_card
        res = client('cart',
            id = options.developer_id,
            stage = '4',
            cart_id = cart_id,
            type = card_type,
            number = card_number,
            exp_month = payment.cc_expiration.month,
            exp_year = payment.cc_expiration.year,
            cvv2 = payment.cc_cvc,
            billing_fname = ' '.join(payment.name_on_card.split()[:-1]),
            billing_lname = payment.name_on_card.split()[-1],
            billing_address = order.billing_address.bill_first_line,
            billing_city = order.billing_address.bill_city,
            billing_state = order.billing_address.bill_state,
            billing_zip = order.billing_address.bill_postal_code,
            billing_country = order.billing_address.bill_country,
            email = order.contact_information.email,
            phone = order.contact_information.phone_number,
            )
        resultcode = res.find('resultcode').text
        if resultcode == '300025':
            return 'Invalid email'
        elif resultcode == '300026':
            return 'Credit card rejected.'
        elif resultcode not in ('000000', '000001'):
            raise Exception('Could not add tickets to cart: %s' % res.find('note').text)
        
        order.user_payment_info_trans_id = cart_id
        return 1 # success

    def capture( self, order, amount ):
        # BPT doesn't provide a separate capture step.
        return 1 # success
    
    def refund( self, order, amount ):
        raise Exception('Not implemented')
