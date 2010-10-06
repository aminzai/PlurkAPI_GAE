from PlurkAPI_User import PlurkUser
import PlurkAPI_tools as tool
try:
    import simplejson as json
except:
    from django.utils import simplejson as json

from datetime import date

class PlurkPlurk:
    """
    ** Singal Plurk **
    """
    def __init__(self, d={}):
        self._data = d
        #c = json.loads( d )
        self.id = d.get('plurk_id', '0')
        # don't parse more until necessary

    def __str__(self):
        #result = 'Plurk(%d): %s\n' % (self.id, self._data)
        result = 'Plurk(%d)%s - %s:\n %s\n' % (
                    self.id, tool.datetime_from_plurk_string(
                        self._data['posted'] ),
                    self._data['owner_id'] ,
                    self._data['content_raw'] )
        #result = [ self.id, self._data['posted'], self._data['owner_id'] ,self._data['content_raw'] ]
        return result.encode('utf8')
        #return result

    def __eq__(self, other):
        if other.__class__ != PlurkPost: return False
        return self._data == other._data

class PlurkPlurkList:
    """
    ***Plurk Post
    A list of plurks and the set of users that posted them.
    """
    def __init__(self, plurk_json_list, user_json_list=[] , CtlDate = False , Date = date.today() ):
        self.plurks = []
        #print plurk_json_list
        #print Date
        if CtlDate == True:
            for x in plurk_json_list:
                #print x
                if Date == tool.datetime_from_plurk_string( x['posted'] ).date() :
                    self.plurks.append( PlurkPlurk( x ) )
        else:
            for x in plurk_json_list:
                self.plurks.append( PlurkPlurk( x ) )

        for x in user_json_list:
            self.users = PlurkUser( x )

    def __iter__(self):
        return self.plurks

    def getPlurks( self ):
        return self.plurks

    def getUsers(self):
        return self.users

    def __eq__(self, other):
        if other.__class__ != PlurkPostList:
            return False
        if self.plurks != other.plurks:
            return False
        if self.users != other.users:
            return False
        return True

