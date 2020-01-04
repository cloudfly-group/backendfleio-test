from fleio.conf import options
from fleio.conf.base import ConfigOpts


class SignUpSettingsConfig(ConfigOpts):
    require_confirmation = options.BoolOpt(default=False)
    email_confirmation_template = options.StringOpt(max_length=64, default='account.signup.confirm')
    allow_free_email_addresses = options.BoolOpt(default=True)
    forbidden_domains_for_email_signup = options.StringOpt(default=None, allow_null=True)
    domains_for_email_signup_whitelist = options.StringOpt(default=None, allow_null=True)

    class Meta:
        section = 'SIGNUP_SETTINGS'


signup_settings = SignUpSettingsConfig()
