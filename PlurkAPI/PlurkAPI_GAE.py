## -*- coding: utf8 -*-

from PlurkAPI import PlurkAPI
from PlurkAPI_Exception import PlurkError
import PlurkAPI_Response
import PlurkAPI_Plurk
import PlurkAPI_User
import PlurkAPI_tools as tool

import urllib
import urllib2
import cookielib
try:
    import simplejson as json
except:
    from django.utils import simplejson as json
import datetime
from datetime import date


class PlurkAPI_GAE(PlurkAPI):
    """
    """
    def __init__(self , ApiKey , DebugLevel=0):

        self._BaseUrl = 'http://www.plurk.com/API'

        self._ApiUrl = {
            'login'             :   '/Users/login',
            'logout'            :   '/Users/logout',
            'getPlurk'          :   '/Timeline/getPlurk',
            'getPlurks'         :   '/Timeline/getPlurks',
            'addPlurk'          :   '/Timeline/plurkAdd',
            'getResponses'      :   '/Responses/get',
            'getCompletionFriendsFans':'/FriendsFans/getCompletion',
            'getOwnProfile'     :   '/Profile/getOwnProfile',
            'getPublicProfile'  :   '/Profile/getPublicProfile'
        }

        PlurkAPI.__init__( self , ApiKey , self._BaseUrl , self._ApiUrl , DebugLevel )

        self.Logined = False

    def login( self , user , passwd ):
        """
        **Login to Plurk**
        Require:
            Username
            Password
        Return:
            1.by self._getStatus
            2.add info to self.UserInfo(PlurkUser)
        """
        if self._CallAPI( 'login' , username = user , password = passwd ) == '200':
            self.UserInfo = PlurkAPI_User.PlurkUser( self._getResult() )
            return self.UserInfo
        else:
            None

    def logout( self ):
        """
        ** Logout
        """
        return self._getReturn()

    def getPlurk( self , plurk_id ):
        """
        **This function just can get only one plurk back**
        Require:
            plurk_id ( not encoded )
        Return:
            Plurk's JSON( python dict )
        """
        self._CallAPI( 'getPlurk' , plurk_id = plurk_id )
        return self._getReturn()

    def getPlurks(self,
                  offset = date.replace( date.today() ) ,
                  limited=False,
                  limit=20,
                  filter=False,
                  only_user= '',
                  CtlDate = False):
        """
        ** Get all plurks in the timeline **
        """
        if '200' == self._CallAPI( 'getPlurks' , offset = tool.conv_datetime( offset ) , limit = limit , only_user=only_user ):
            #print 'run'
            #print '='*50
            #print self._getResult()['plurks']
            #print '='*50
            return PlurkAPI_Plurk.PlurkPlurkList( self._getResult()['plurks'] ,CtlDate=CtlDate , Date = offset)
        else:
            return 'Status:',self._getStatus()

    def getOwnProfile( self ):
        """
        Get Own Profile
        """
        if self._CallAPI( 'getOwnProfile') == '200':
            return PlurkAPI_User.PlurkUser( self._getResult() )
        else:
            None

    def getPublicProfile( self , user_id ):
        """
        ** Get somebody public profile **
        """
        if self._CallAPI( 'getPublicProfile',user_id = user_id ) == '200':
            return PlurkAPI_User.PlurkUser( self._getResult() )
        else:
            None

    def getCompletionFriendsFans(self):
        """
        ** Get completetion friends and fans
        """
        if self._CallAPI( 'getCompletionFriendsFans' ) == '200':
            #return PlurkAPI_User.PlurkUser( self._getResult() )
            return  self._getResult()
        else:
            None


    def addPlurk( self , lang='en' , qualifier='says' , content='Test' ):
        """
        ** Add a plurk **
        """
        self._CallAPI( 'addPlurk' ,
                      lang = lang,
                      qualifier = qualifier,
                      content = content )
        return self._getReturn()

    def getResponses( self , plurk_id ):
        """
        ** Get plurk's responses
        """
        self._CallAPI( 'getResponses' , plurk_id = plurk_id )
        return PlurkAPI_Response.PlurkResponseList( self._getResult() )
        #return self._getReturn()

