from typing import Optional


def current_activity_id() -> Optional[int]:
    from fleio.activitylog.utils.activity_helper import activity_helper

    return activity_helper.get_current_activity_log_id()


def set_current_activity_if_none(activity_id: int) -> bool:
    from fleio.activitylog.utils.activity_helper import activity_helper

    if not activity_helper.has_current_activity():
        activity_helper.set_current_activity(activity_id=activity_id)
        return True

    return False


def end_current_activity(activity_id: int):
    from fleio.activitylog.utils.activity_helper import activity_helper

    return activity_helper.end_activity()
