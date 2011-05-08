from zope import schema
from getpaid.core import interfaces


class IBPTOptions(interfaces.IPaymentProcessorOptions):
    
    developer_id = schema.ASCIILine(title = u'Developer ID')
    test_mode = schema.Bool(
        title = u'Send cart to BPT in test mode',
        default = True
        )


class IBPTEventLineItem(interfaces.ILineItem):
    """Marker for Brown Paper Tickets event items"""
