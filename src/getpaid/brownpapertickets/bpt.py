from urllib import urlencode, urlopen
from xml.etree import ElementTree


class BrownPaperTicketsClient(object):
    endpoint = 'https://www.brownpapertickets.com/api2/'
    
    def __call__(self, method, **kw):
        query = urlencode(kw)
        url = '%s/%s?%s' % (self.endpoint, method, query)
        res = urlopen(url).read()
        if len(res.splitlines()) > 1:
            return ElementTree.fromstring(res)
