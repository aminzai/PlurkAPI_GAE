class PlurkUser:
    def __init__( self , PersionInfo = {} ):
        if PersionInfo.has_key('user_info'):
            UserInfo = PersionInfo['user_info']
        else:
            UserInfo = PersionInfo


        self.uid = UserInfo.get('uid', 0)
        self.id = UserInfo.get('id', 0)
        self.username = UserInfo.get('nick_name', '')
        self.birth = UserInfo.get('date_of_birth','')

        self.stats = {}
        for key in ('fans_count', 'friends_count', 'alerts_count','unread_count'):
            self.stats[key] = PersionInfo.get(key, '0')
        for key in ('recruited','karma'):
            self.stats[key] = UserInfo.get(key, '0')

        self.settings = {}
        for key in ('privacy','has_read_permission'):
            self.settings[key] = PersionInfo.get(key , '')
        for key in ('display_name', 'relationship', 'has_profile_image', 'avatar',
                    'date_of_birth', 'location', 'full_name', 'gender', 'timezone'):
            self.settings[key] = UserInfo.get(key, None)
        self.plurks = PersionInfo.get('plurks', [])
