import json
from keystoneauth1.identity.generic.password import Password
from keystoneauth1.session import Session


class FleioKeystoneAuthPlugin(Password):
    def __init__(self, auth_url, project_id, project_domain_id, admin_username, admin_password,
                 admin_domain_id=None, api_version='3',
                 identity_type='identity', cache=None):

        super(FleioKeystoneAuthPlugin, self).__init__(auth_url=auth_url,
                                                      project_id=project_id,
                                                      project_domain_id=project_domain_id,
                                                      username=admin_username,
                                                      password=admin_password,
                                                      user_domain_id=admin_domain_id)
        self.api_version = api_version
        self.identity_type = identity_type
        self.cache = cache

    def get_auth_ref(self, session, **kwargs):
        access_obj = super(FleioKeystoneAuthPlugin, self).get_auth_ref(session, **kwargs)
        if self.cache and access_obj:
            cache_id = self.get_cache_id()
            data = {'auth_token': access_obj.auth_token,
                    'body': access_obj._data}
            self.cache[cache_id] = json.dumps(data)
        return access_obj

    def get_access(self, session, **kwargs):
        if self.cache:
            cache_id = self.get_cache_id()
            self.set_auth_state(self.cache.get(cache_id, None))
        return super(FleioKeystoneAuthPlugin, self).get_access(session, **kwargs)

    def get_cache_id_elements(self):
        return {'auth_url': self.auth_url,
                'project_id': self._project_id,
                'project_domain_id': self._project_domain_id}

    def invalidate(self):
        self.cache = None
        return super(FleioKeystoneAuthPlugin, self).invalidate()


def get_session(auth_url, project_id, project_domain_id, admin_username,
                admin_password, admin_domain_id, api_version='3',
                identity_type='identity', original_ip=None, verify=False, cache=None, timeout=None):

    assert project_id, 'Invalid project received for keystone session: {}'.format(project_id)

    auth_plugin = FleioKeystoneAuthPlugin(auth_url=auth_url,
                                          project_id=project_id,
                                          project_domain_id=project_domain_id,
                                          admin_username=admin_username,
                                          admin_password=admin_password,
                                          admin_domain_id=admin_domain_id,
                                          api_version=api_version,
                                          identity_type=identity_type,
                                          cache=cache)

    return Session(auth=auth_plugin, original_ip=original_ip, verify=verify, timeout=timeout)
