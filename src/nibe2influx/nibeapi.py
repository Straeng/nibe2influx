import json
from requests_oauthlib import OAuth2Session


class NibeApi:
    '''
    TODO: Currently assumes that authorization is already done and
    there is a tokej.json file.
    '''

    _BASE_URL        = 'https://api.nibeuplink.com'
    _TOKEN_URL       = _BASE_URL+'/oauth/token'
    _API_URL         = _BASE_URL+'/api/v1'

    def __init__(self, conf, token_file):

        self.sysid = conf['system_id']
        self.token_file = token_file

        client_conf = conf['client']

        token = self.recall_token()
    
        self.session = OAuth2Session(
            client_id            = client_conf['client_id'],
            redirect_uri         = conf['redirect_uri'],
            auto_refresh_url     = self._TOKEN_URL,
            auto_refresh_kwargs  = client_conf,
            scope                = [ 'READSYSTEM' ],
            token                = token,
            token_updater        = self.persist_token
        )

        if not token:
            self.request_new_token(client_conf['client_secret'])

    def persist_token(self, token):
        with open(self.token_file, 'w') as tf:
            json.dump(token, tf)

    def recall_token(self):
        try:
            with open(self.token_file) as tf:
                token = json.load(tf)
                if 'access_token' in token and 'refresh_token' in token:
                    return token
                else:
                    return None
        except:
            # TODO
            print("ERROR: Currently requires a pre-existing token file.")
            exit(1)
            return None

    def get(self, res, params):
        url = '{}{}'.format(self._API_URL, res)
        result = self.session.get(url, params=params, headers={})

        return result.json()
        

    def request_new_token(self, client_secret):
        token = self.session.fetch_token(self._TOKEN_URL,
                client_secret = client_secret,
                authorization_response = '') #TODO

        print(token)
        self.persist_token(token)

        return token
        

    def get_categories(self):
        return self.get('/systems/{}/serviceinfo/categories'.format(self.sysid), {})


    def get_category(self, cid):
        return self.get('/systems/{}/serviceinfo/categories/{}'.format(self.sysid, cid), {})

    def get_parameters(self, paramlist):
        return self.get('/systems/{}/parameters'.format(self.sysid), {'parameterIds':paramlist})