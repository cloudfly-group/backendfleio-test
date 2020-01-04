from fleio.conf import options
from fleio.conf.base import ConfigOpts


class SFASettingsConfig(ConfigOpts):
    require_end_users_to_use_sfa = options.BoolOpt(default=False)
    require_staff_users_to_use_sfa = options.BoolOpt(default=False)

    class Meta:
        section = 'SFA_SETTINGS'


sfa_settings = SFASettingsConfig()
