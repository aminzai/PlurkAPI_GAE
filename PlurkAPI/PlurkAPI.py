# -*- coding: utf8 -*-

from PlurkAPI_Exception import PlurkError

import urllib
import urllib2
import cookielib
try:
    import simplejson as json
except:
    from django.utils import simplejson as json


class PlurkAPI:
    """
    """
    class HttpErrorHandler(urllib2.BaseHandler):
        '''Error handler class for http protocol used in PlurkConnection'''
        def __init__(self):
            self._status_code = 0
            self._response_body = ''
        def http_error_400(self, req, fp, code, msg, hdrs):
            self._status_code = code
            self._response_body = fp.read()

    def __init__(self , ApiKey , BaseUrl , ApiUrl , DebugLevel=0):
        self._ApiKey = ApiKey
        self._BaseUrl = BaseUrl
        self._ApiUrl = ApiUrl
        self._DebugLevel = DebugLevel

        self._http_error_handler = self.HttpErrorHandler()
        self._cookies = cookielib.CookieJar()
        http = urllib2.HTTPHandler()
        https = urllib2.HTTPSHandler()
        http.set_http_debuglevel( self._DebugLevel )
        https.set_http_debuglevel( self._DebugLevel )
        self._opener = urllib2.build_opener(
                        http,
                        https,
                        self._http_error_handler,
                        urllib2.HTTPCookieProcessor(self._cookies))

        self._status_code = ''
        self._result = ''

    def _getUrl( self , request , encrypt = False ):
        """
        get url back
        """
        if self._ApiUrl.has_key( request ):
            return self._BaseUrl + self._ApiUrl[ request ]
        else:
            raise PlurkError, "Can't not find is url request: "+ request

    def _CallAPI( self , request ,  encrypt = False , **params):
        if not params.has_key('api_key'):
            params['api_key'] = self._ApiKey
        url = self._getUrl(request, encrypt)
        self._Connect( url , **params )
        return self._getStatus()

    def _Connect( self , url , **params ):
        try:
            #print params
            self._result = self._opener.open( url , urllib.urlencode( params ) ).read()
            self._status_code = '200'
            self._error_msg = ''
        except urllib2.HTTPError, e:
            self._status_code = e.code
            self._error = e.msg
            self._body = self._http_error_handler._response_body
        except urllib2.URLError, e:
            self._status_code = e.code
            self._error = e.reason
            self._result = self._http_error_handler._response_body

    def _getStatus( self ):
        """
        ** Get Status
        """
        return self._status_code

    def _getErrorMsg( self ):
        """
        ** Get Error Message
        """
        return self._error + self._fp

    def _getResult( self ):
        """
        ** Get self._fp result by simplejson.loads()
        Require:
            None
        Return:
            a JSON dict
        """
        return json.loads( self._result )

    def _getReturn( self ):
        """
        """
        if '200' == self._getStatus():
            return self._getResult()
        else:
            return None

