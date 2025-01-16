from urllib.parse import parse_qs, urlparse
from werkzeug.datastructures import ImmutableMultiDict

class MicrosoftService():
    
    def __init__(self):
        pass
    
    def get_data_for_login(self, request_body):
        pathname = request_body["pathname"]
        parse_res = urlparse(pathname)
        query_params = parse_qs(parse_res.query)
        login_data = ImmutableMultiDict(
            [
                ('code', query_params["code"][0]),
                ('client_info', query_params["client_info"][0]),
                ('state', query_params["state"][0]),
            ]
        )
        
        return login_data
    