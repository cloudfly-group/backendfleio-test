from django.utils.translation import ugettext_lazy as _

NOTIFICATION_DISPLAY_NAMES = {
    'account.credit.low': _('Account credit low'),
    'account.reset.password': _('Account reset password'),
    'account.signup.confirm': _('Account signup confirmation'),
    'account.suspended': _('Account suspended'),

    'billing.invoice.new': _('Billing new invoice'),

    'ticket.enduser.opened': _('Ticket opened'),
    'ticket.enduser.reply': _('Ticket reply added'),
    'ticket.enduser.closed': _('Ticket closed'),

    'ticket.staff.opened': _('Ticket opened'),
    'ticket.staff.reply': _('Ticket reply added'),
    'ticket.staff.closed': _('Ticket closed'),

    'openstack.error': _('Openstack error'),

    'staff.new_order': _('New order placed'),
    'staff.new_payment': _('New payment added'),
}


class NotificationTemplatesHelpText:
    help_text_map = {
        'account.credit.low': {
            'detail': _('This notification template will be sent to the user if his account is running low on' +
                        ' credit. This will inform him how much time his credit will last based on the active' +
                        ' cloud resources he has. Available variables to use are:'),
            'variables': ['{{ variables.credit }}', '{{ variables.currency }}', '{{ variables.credit_hours_left }}',
                          '{{ variables.add_credit_url }}']
        },
        'account.reset.password': {
            'detail': _('This notification template will be sent to the user if he requests password change for his' +
                        ' account, in case he forgets it. Available variables to use are:'),
            'variables': ['{{ user.first_name }}', '{{ user.last_name }}', '{{ frontend_url }}', '{{ user_id }}',
                          '{{ token }}']
        },
        'account.signup.confirm': {
            'detail': _('This notification template will be sent to the user right after registration in order to '
                        'confirm his account. Available variables to use are:'),
            'variables': ['{{ variables.frontend_url }}', '{{ variables.first_name }}',
                          '{{ variables.confirmation_token }}', ]
        },
        'account.suspended': {
            'detail': _('Notification to be sent if the cloud resources related to a client have been suspended' +
                        ' because he ran out of credit. Available variables to use are:'),
            'variables': ['{{ variables.add_credit_url }}']
        },
        'billing.invoice.new': {
            'detail': _('Notification that is sent when a user orders a new product and an invoice gets issued.' +
                        ' Available variables to use are:'),
            'variables': ['{{ variables.invoice_id }}', '{{ variables.amount }}', '{{ variables.currency }}',
                          '{{ variables.invoice_url }}', '{{ variables.display_number }}']
        },
        'ticket.staff.closed': {
            'detail': _('This notification will be sent when a ticket was closed to either staff users or bcc '
                        'recipients that are defined in the ticket. Available variables to use are:'),
            'variables': ['{{ variables.ticket_id }}', '{{ variables.ticket_title }}', '{{ variables.ticket_url }}']
        },
        'ticket.staff.opened': {
            'detail': _('This notification will be sent when a ticket is opened to either staff users or bcc '
                        'recipients that are defined in the ticket. Available variables to use are:'),
            'variables': ['{{ variables.ticket_id }}', '{{ variables.ticket_title }}', '{{ variables.ticket_body }}',
                          '{{ variables.ticket_url }}', '{{ variables.ticket_created_by }}', ]
        },
        'ticket.staff.reply': {
            'detail': _('This notification will be sent when a ticket receives a reply to either staff users or bcc '
                        'recipients that are defined in the ticket. '
                        'Available variables to use are:'),
            'variables': ['{{ variables.ticket_id }}', '{{ variables.ticket_update_owner }}',
                          '{{ variables.ticket_update_body }}', '{{ variables.ticket_title }}',
                          '{{ variables.ticket_url }}']
        },
        'ticket.enduser.closed': {
            'detail': _('This notification will be sent when a ticket was closed to either the enduser or cc '
                        'recipients that are defined in the ticket. Available variables to use are:'),
            'variables': ['{{ variables.ticket_id }}', '{{ variables.ticket_title }}', '{{ variables.ticket_url }}']
        },
        'ticket.enduser.opened': {
            'detail': _('This notification will be sent when a ticket is opened to either the enduser or cc '
                        'recipients that are defined in the ticket. Available variables to use are:'),
            'variables': ['{{ variables.ticket_id }}', '{{ variables.ticket_title }}', '{{ variables.ticket_body }}',
                          '{{ variables.ticket_url }}', '{{ variables.ticket_created_by }}', ]
        },
        'ticket.enduser.reply': {
            'detail': _('This notification will be sent when a ticket receives a reply to either the enduser or cc '
                        'recipients that are defined in the ticket. Available variables to use are:'),
            'variables': ['{{ variables.ticket_id }}', '{{ variables.ticket_update_owner }}',
                          '{{ variables.ticket_update_body }}', '{{ variables.ticket_title }}',
                          '{{ variables.ticket_url }}']
        },
        'staff.new_order': {
            'detail': _('This notification will be sent to staff users when a new order is placed by a client.'),
            'variables': [
                '{{ variables.frontend_url }}', '{{ variables.client_name }}',
                '{{ variables.client_id }}', '{{ variables.order_id }}',
            ]
        },
        'staff.new_payment': {
            'detail': _('This notification will be sent to staff users when a new payment is made by a client.'),
            'variables': [
                '{{ variables.frontend_url }}', '{{ variables.client_name }}', '{{ variables.client_id }}',
                '{{ variables.journal_id }}'
            ]
        },
    }
