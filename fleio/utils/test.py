import os
import zipfile
from os.path import dirname

import requests
from django.conf import settings


# noinspection PyUnresolvedReferences
def backup_current_license(name):
    with zipfile.ZipFile(name, mode='w') as license_zip:
        current_dir = dirname(dirname(__file__))
        core_view_path = os.path.join(current_dir, 'core/')
        collector_path = os.path.join(current_dir, 'osbilling/bin/')

        if os.path.isfile(os.path.join(core_view_path, 'loginview.py')):
            license_zip.write(os.path.join(core_view_path, 'loginview.py'))
        elif os.path.isfile(os.path.join(core_view_path, 'loginview.so')):
            license_zip.write(os.path.join(core_view_path, 'loginview.py'))

        license_zip.write(os.path.join(core_view_path, 'utils'))

        if os.path.isfile(os.path.join(collector_path, 'collectorlib.so')):
            license_zip.write(os.path.join(collector_path, 'collectorlib.so'))
        elif os.path.isfile(os.path.join(collector_path, 'collectorlib.py')):
            license_zip.write(os.path.join(collector_path, 'collectorlib.py'))


def make_license_version_on_server(version, commit_id=None):
    url = settings.LICENSING_SERVER_URL + 'licenseop/make-license-version'
    response = requests.post(url, data={'version': version, 'commit_id': commit_id},
                             proxies=settings.PROXY_SETTINGS, timeout=(10, 60))
    assert response.status_code == 200


def remove_license_version_on_server(version):
    url = settings.LICENSING_SERVER_URL + 'licenseop/make-license-version'
    response = requests.post(url, data={'version': version},
                             proxies=settings.PROXY_SETTINGS, timeout=(10, 60))
    assert response.status_code == 200


def restore_current_license(name):
    with zipfile.ZipFile(name, mode='r') as license_zip:
        license_zip.extractall('/')
    os.remove(name)


def get_a_license():
    # noinspection SpellCheckingInspection
    url = settings.LICENSING_SERVER_URL + 'licenseop/get-trial-license/{0}'.format('testtest_user_testtest')
    response = requests.get(url, proxies=settings.PROXY_SETTINGS, timeout=(10, 60))
    assert response.status_code == 200
    return response.content.decode("utf-8")


# noinspection PyUnresolvedReferences
def remove_live_license():
    current_dir = dirname(dirname(__file__))
    core_view_path = os.path.join(current_dir, 'core/')
    collector_path = os.path.join(current_dir, 'osbilling/bin/')

    try:
        os.remove(os.path.join(core_view_path, 'loginview.so'))
    except (IOError, OSError):
        os.remove(os.path.join(core_view_path, 'loginview.py'))

    os.remove(os.path.join(core_view_path, 'utils'))

    try:
        # noinspection PyUnresolvedReferences
        os.remove(os.path.join(collector_path, 'collectorlib.so'))
    except (IOError, OSError):
        os.remove(os.path.join(collector_path, 'collectorlib.py'))


class LogMockBuilder:
    """
    Use this class to:

      * hide expected error logs from tests output (matched with 'startswith', not necessarly the while string)
      * be sure that expected errors are actually logged: len (mocked_but_not_logged()) == 0
      * no other other errors are logged than the ones expected: len(logged_but_not_mocked()) == 0

    Known issue:
      * if you change the error log messages in code, tests may fail
    """
    def __init__(self, original_callable, mocked_strings, pass_other_strings=True):
        """
        Mock calls to :param mocked_strings: that are called with the first parameter starting with ong of
        :param mocked_strings:.
        Useful to hide some of the errors logs, depending on logeed string.
        Also tracks strings that have been used in calls.

        :param origina_callable: original calable that is being mocked
        :param mocked_strings: one string or a list of strings to check against the
        """
        self.original_callable = original_callable
        if isinstance(mocked_strings, str):
            self.mocked_strings_list = (mocked_strings,)
        else:
            self.mocked_strings_list = mocked_strings
        self.pass_other_strings = pass_other_strings
        self.strings_in_call = dict()

    def __call__(self, *args, **kwargs):
        param1 = args[0]

        if self._match_string(str(param1)):
            # string matched
            pass
        elif self.pass_other_strings:
            # string not matched and invoking original callable
            return self.original_callable(*args, **kwargs)

    def _record_call_string(self, call_str):
        self.strings_in_call[call_str] = self.strings_in_call.get(call_str, 0) + 1

    def _match_string(self, param1):
        matched = False
        for mocked_str in self.mocked_strings_list:
            if param1.startswith(mocked_str):
                matched = True
                break

        if matched:
            self._record_call_string(mocked_str)
        else:
            self._record_call_string(param1)

        return matched

    def mocked_but_not_logged(self):
        """Returns True if all the mocked strings were logged"""
        not_logged = list()
        for mocked_str in self.mocked_strings_list:
            if mocked_str not in self.strings_in_call:
                not_logged.append(mocked_str)
        return not_logged

    def logged_but_not_mocked(self):
        """Returns True if no other string than the mocked one were logged"""
        not_mocked = list()
        for call_str in self.strings_in_call:
            if call_str not in self.mocked_strings_list:
                not_mocked.append(call_str)
        return not_mocked

    def assertAllAndOnly(self):
        not_logged_errors = self.mocked_but_not_logged()
        assert len(not_logged_errors) == 0,\
            'The following logs were mocked but not logged: {}'.format(not_logged_errors)

        not_mocked_errors = self.logged_but_not_mocked()
        assert len(not_mocked_errors) == 0,\
            'The following logs were logged but not mocked: {}'.format(not_mocked_errors)
