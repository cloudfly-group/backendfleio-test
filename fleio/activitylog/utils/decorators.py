from functools import partial
import logging
from typing import Optional

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin

from fleio.activitylog.formatting import add_additional_activities
from fleio.activitylog.formatting import add_default_activities
from fleio.activitylog.formatting import get_log_class_name
from fleio.activitylog.formatting import logclass_text
from fleio.activitylog.operations import fetch_log_category
from fleio.activitylog.utils.activity_helper import activity_helper

LOG = logging.getLogger(__name__)


def _log_activity(
        view_class, category_name: str, user_type: str, object_name: str, object_name_plural: str,
        additional_activities: Optional[dict],
):
    add_default_activities(user_type=user_type, object_name=object_name, object_name_plural=object_name_plural)
    add_additional_activities(
        user_type=user_type, object_name=object_name, object_name_plural=object_name_plural,
        additional_activities=additional_activities,
    )

    def _initial_wrapper(self, request: Request, *args, **kwargs):
        viewset = self  # type: ViewSetMixin
        logclass_name = get_log_class_name(
            activity_name=viewset.action,
            user_type=user_type,
            object_name=object_name,
        )
        log_category = self.get_log_category()
        if logclass_name in logclass_text:
            object_id = kwargs.get(self.lookup_field, None)
            activity_helper.start_view_activity(
                activity_category=log_category,
                activity_class=logclass_name,
                request=request,
                object_id=object_id,
            )

        return self._original_initial(
            request=request, *args, **kwargs,
        )

    def _finalize_response_wrapper(self, request: Request, response: Response, *args, **kwargs):
        if activity_helper.has_current_activity():
            if response.status_code >= 200 and response.status_code < 300:
                action = getattr(self, 'action', None)
                if action == 'create':
                    response_data = getattr(response, 'data', None)
                    if response_data and hasattr(response_data, 'get'):
                        object_id = response_data.get('id', None)
                        if object_id:
                            activity_helper.add_current_activity_params(object_id=object_id)
                activity_helper.end_activity()
            else:
                activity_helper.end_activity(failed=True)

        return self._original_finalize_response(request=request, response=response, *args, **kwargs)

    def get_log_category(self):
        if not getattr(self, 'log_category', None):
            self.log_category = fetch_log_category(category_name)
        return self.log_category

    if not issubclass(view_class, APIView):
        raise TypeError('log_activity decorator should be only applied to classes derived from APIView')
    if not issubclass(view_class, ViewSetMixin):
        raise TypeError('log_activity decorator should be only applied to classes derived from ViewSetMixin')

    if hasattr(view_class, '_original_initial') and hasattr(view_class, '_original_finalize_response'):
        LOG.warning('Decorator already applied on view class, restoring functions')
        # noinspection PyProtectedMember
        view_class.initial = view_class._original_initial
        # noinspection PyProtectedMember
        view_class.finalize_response = view_class._original_finalize_response

    # override functions
    view_class._original_initial = view_class.initial
    view_class._original_finalize_response = view_class.finalize_response
    view_class.initial = _initial_wrapper
    view_class.finalize_response = _finalize_response_wrapper
    view_class.get_log_category = get_log_category

    return view_class


def log_staff_activity(
    category_name: str, object_name: str, object_name_plural: Optional[str] = None,
    additional_activities: Optional[dict] = None,
):
    if not object_name_plural:
        object_name_plural = object_name + 's'
    return partial(
        _log_activity, category_name=category_name, user_type='staff',
        object_name=object_name, object_name_plural=object_name_plural,
        additional_activities=additional_activities,
    )


def log_reseller_activity(
    category_name: str, object_name: str, object_name_plural: Optional[str] = None,
    additional_activities: Optional[dict] = None,
):
    if not object_name_plural:
        object_name_plural = object_name + 's'
    return partial(
        _log_activity, category_name=category_name, user_type='reseller',
        object_name=object_name, object_name_plural=object_name_plural,
        additional_activities=additional_activities,
    )


def log_enduser_activity(
    category_name: str, object_name: str, object_name_plural: Optional[str] = None,
    additional_activities: Optional[dict] = None,
):
    if not object_name_plural:
        object_name_plural = object_name + 's'
    return partial(
        _log_activity, category_name=category_name, user_type='enduser',
        object_name=object_name, object_name_plural=object_name_plural,
        additional_activities=additional_activities,
    )
