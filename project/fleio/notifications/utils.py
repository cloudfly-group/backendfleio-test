from fleio.notifications.models import Notification


def reset_current_notification(client, notification_name: str, priority: str):
    """sets is_current to False before a new is_current notification gets created"""
    notification = Notification.objects.filter(
        client=client,
        name=notification_name,
        priority=priority,  # priority is important because notifications with same name may differentiate using this
    ).order_by('generated').last()
    if notification:
        if notification.is_current:
            notification.is_current = False
            notification.save()
