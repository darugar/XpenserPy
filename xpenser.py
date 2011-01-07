import urllib, urllib2
from django.utils import simplejson

class Xpenser:
    BASE_URL    = 'https://www.xpenser.com/api/v1.0/'

    def __init__(self, username, passwd):
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.BASE_URL, username, passwd)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

    def _request(self, request, params=None):
        print "Hello: _request", request, params
        try:
            req = urllib2.Request(self.BASE_URL + request, params)
            conn  = urllib2.urlopen(req)
            print "Response ", conn.code, conn.msg
            response = conn.read()
        except Exception, e:
            print "Unable to make request: [%s]: [%s]" % (str(e), e.read())
            raise
        try:
            result = simplejson.loads(response)
        except Exception, e:
            print "Unable to process response: [%s]" % (str(e), )
            print response
            raise
        return result

    def get_expenses(self, params=""):
        ''' '''
        try:
            result = self._request('expenses/?' + params)
        except Exception, e:
            print "Unable to get expenses:", str(e)
            return False
        return result

if __name__ == "__main__":
    xp = Xpenser('username@something.com', 'password')
    expenses = xp.get_expenses()
    print "Here are your expenses:"
    for expense in expenses:
        print expense['type'], expense['amount'], expense['date']
    
    print "Expenses modified since 2010-09-28 in any report"
    new_expenses = xp.get_expenses('modified=2010-09-28+00:00:00&modified_op=gt&report=*')
    for expense in new_expenses:
        print expense['type'], expense['amount'], expense['date']
