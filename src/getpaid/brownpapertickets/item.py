from zope.interface import implements
from getpaid.core.item import PayableLineItem
from getpaid.brownpapertickets.interfaces import IBPTEventLineItem


class BPTEventLineItem(PayableLineItem):
    implements(IBPTEventLineItem)
