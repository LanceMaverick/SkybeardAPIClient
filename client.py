import requests

class NoAPIKeyError:
    pass

def check_auth(func):
    def inner(self, *args, **kwargs):
        if not self.key:
            raise NoAPIKeyError('No api key set')
        else:
            return func(self, *args, **kwargs)
    return inner

class BeardApiClient:
    def __init__(self, **kwargs):
        url = kwargs['url']
        if 'http://' not in url:
            self.base_url = 'http://'+url
        else:
            self.base_url = url
        self.base_url = kwargs['url']
        self.key = kwargs.get('key', None)
        self.default_chat = kwargs.get('default_chat', None)
    
    @check_auth
    def send_message(self, text, chat_id = None):
        if not chat_id:
            try:
                chat_id = self.default_chat
            except ValueError as e:
                print('No chat_id or default_chat defined')
                raise(e)
        payload = {
                'chat_id': str(chat_id),
                'text': text
                }
        url = '{}/key{}/relay/sendMessage'.format(
                self.base_url,
                self.key)
        print(url)
        response = requests.post(url, json = payload)
        return response
