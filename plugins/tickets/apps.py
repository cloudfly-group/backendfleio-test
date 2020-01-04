from django import apps
from django.utils.translation import ugettext_lazy as _

from fleio.core.plugins.plugin_definition import MenuItem
from fleio.core.plugins.plugin_definition import PluginDefinition
from fleio.core.plugins.plugin_definition import PluginConfigTypes


class TicketsPluginConfig(apps.AppConfig):
    name = 'plugins.tickets'
    verbose_name = 'Tickets'

    plugin_definition = None

    @classmethod
    def initialize_plugin(cls) -> PluginDefinition:
        if not cls.plugin_definition:
            definition = PluginDefinition(
                display_name=_('Tickets'),
                app_name=cls.name,
                app_label='tickets',
                feature_name='plugins.tickets',
                staff_feature_name='plugins.tickets',
            )

            # Staff plugin menu definition
            definition.add_menu_item(config_type=PluginConfigTypes.staff, menu_item=MenuItem(
                label=_('Tickets'),
                state='pluginsTicketsTickets',
                icon='tickets',
                feature='plugins.tickets',
                plugin_name='tickets',
            ))

            definition.add_menu_item(config_type=PluginConfigTypes.staff, menu_item=MenuItem(
                label=_('Departments'),
                state='pluginsTicketsDepartments',
                icon='group',
                feature='plugins.tickets',
                plugin_name='tickets',
            ))

            # Enduser plugin menu definition
            definition.add_menu_item(config_type=PluginConfigTypes.enduser, menu_item=MenuItem(
                label=_('Tickets'),
                state='pluginsTicketsTickets',
                icon='tickets',
                feature='plugins.tickets',
                plugin_name='tickets',
            ))

            # Staff urls
            definition.add_url_config(
                config_type=PluginConfigTypes.staff,
                module_name='plugins.tickets.staff.urls',
                path='tickets',
                namespace='tickets'
            )

            # Enduser urls
            definition.add_url_config(
                config_type=PluginConfigTypes.enduser,
                module_name='plugins.tickets.enduser.urls',
                path='tickets',
                namespace='tickets'
            )

            cls.plugin_definition = definition

        # clean some of the obsolete attachments if they exist whenever django starts
        # TODO: maybe add a cron for this?
        from plugins.tickets.models.attachment import Attachment
        obsolete_attachments = Attachment.objects.filter(
            ticket=None, ticket_update=None, ticket_note=None, email_message=None
        ).order_by('id')[:10]
        for attachment in obsolete_attachments:
            attachment.delete()

        return cls.plugin_definition
