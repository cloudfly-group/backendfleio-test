from fleio.conf import options
from fleio.conf.base import ConfigOpts


class TermsOfServiceSettingsConfig(ConfigOpts):
    require_end_users_to_agree_with_latest_tos = options.BoolOpt(default=False)
    ask_again_after = options.IntegerOpt(min=0, default=43800)
    forbid_access_after = options.StringOpt(default='', allow_null=True)

    class Meta:
        section = 'TOS_SETTINGS'


tos_settings = TermsOfServiceSettingsConfig()
