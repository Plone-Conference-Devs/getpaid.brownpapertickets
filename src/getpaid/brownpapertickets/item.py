from zope.interface import implements
from getpaid.core.item import LineItem
from getpaid.brownpapertickets.interfaces import IBPTEventLineItem


class BPTEventLineItem(LineItem):
    implements(IBPTEventLineItem)
