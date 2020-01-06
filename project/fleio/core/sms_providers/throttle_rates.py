from rest_framework import throttling


class SMSSendingRateThrottle(throttling.UserRateThrottle):
    scope = 'sms_sending'
