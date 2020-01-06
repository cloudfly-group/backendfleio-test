from ipware.ip import get_ip


class OrderMetadata:
    """Metadata for an order to be used by anti fraud or other modules"""
    def __init__(self, ip_address, user_agent, accept_language, session_id):
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.accept_language = accept_language or 'en-US,en;q=0.8'
        self.session_id = session_id

    def to_json(self):
        return {'ip_address': self.ip_address,
                'user_agent': self.user_agent,
                'accept_language': self.accept_language,
                'session_id': self.session_id}

    @classmethod
    def from_request(cls, request):
        session_id = getattr(request.session, 'session_key', None)
        return cls(ip_address=get_ip(request=request),
                   user_agent=request.META.get('HTTP_USER_AGENT'),
                   accept_language=request.META.get('HTTP_ACCEPT_LANGUAGE', 'en-US,en;q=0.8'),
                   session_id=session_id)

    @classmethod
    def from_json(cls, json_metadata):
        return cls(ip_address=json_metadata.get('ip_address'),
                   user_agent=json_metadata.get('user_agent'),
                   accept_language=json_metadata.get('accept_language'),
                   session_id=json_metadata.get('session_id'))
