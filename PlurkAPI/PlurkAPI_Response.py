# -*- coding: utf8 -*-

from PlurkAPI_User import PlurkUser
#import jsonizer
import PlurkAPI_tools as tool

class PlurkResponse:
    """
    A response to a plurk. Attributes: lang, content_raw, user_id, qualifier,
    plurk_id, content, id, posted.
    """
    def __init__(self, PersionInfo):
        self.__dict__.update(PersionInfo)
        if self.__dict__.has_key('posted') and type(self.posted) == str:
            self.posted = tool.datetime_from_plurk_string(self.posted)
    def __str__(self):
        result = u'%s%s %s' % (self.user_id, ' '+self.qualifier+':' if self.qualifier != ':' else ':', self.content_raw)
        return result.encode('utf8')

class PlurkResponseList:
    """
    A list of responses to a plurk and their posters.
    """
    def __init__(self, PersionInfo):
        """
        Construct a PlurkResponse from a dictionary.
        """
        self.datadict = PersionInfo
        self.num_responses = PersionInfo['responses_seen']
        self.response_list = [PlurkResponse(dic) for dic in PersionInfo['responses']]
        fdict = PersionInfo['friends']   # dict of friends who posted responses
        self.poster_dict = dict((int(k),PlurkUser(v)) for k,v in fdict.iteritems())

    def __iter__(self):
        return self.response_list.__iter__()

    def __str__(self):
        result = [u'responses [']
        result.append(u', '.join([u'%s%s %s\n' % (
            self.poster_dict[r.user_id].username,
            r.qualifier if r.qualifier == ':' else ' '+r.qualifier+':',
            r.content_raw) for r in self.response_list]))
        result.append(u']')
        return u''.join(result).encode('utf8')

    def getAllResponser( self ):
        #tmp = {}
        #for r in self.response_list:
        #    tmp[r.user_id]=0

        #return tmp.keys()
        #return ['%s' % ( self.poster_dict[r.user_id].username ) for r in self.response_list]
        return ['%s' % ( r.user_id ) for r in self.response_list]

    def __eq__(self, other):
        return self.__class__ == other.__class__ and \
               self.num_responses == other.num_responses and \
               self.response_list == other.response_list and \
               self.poster_dict == other.poster_dict
