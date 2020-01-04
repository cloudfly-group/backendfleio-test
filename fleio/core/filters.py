import datetime

from django.db.models import Q
from django.core.exceptions import FieldError

from rest_framework import filters

from fleio.core.exceptions import APIBadRequest


class CustomFilter(filters.BaseFilterBackend):
    values_map = {
        'null': None,
        'true': True,
        'false': False
    }

    @staticmethod
    def get_filtered_queryset(queryset, filtering):
        if filtering:
            filtering = filtering.split('+')
            for i in range(len(filtering)):
                filtering[i] = filtering[i].split(':')
            keys = {}
            for item in filtering:
                key = item[0]
                value = item[1]
                if key.endswith('__ne'):
                    filter_params = dict()
                    key = key[:-4]
                    value = CustomFilter.values_map.get(value.lower(), value)
                    filter_params[key] = value
                    queryset = queryset.exclude(**filter_params)
                else:
                    value = CustomFilter.values_map.get(value.lower(), value)
                    if key.endswith('__date'):
                        key = key[:-6]
                        date_object = value.split(',')
                        year = date_object[0]
                        month = date_object[1]
                        day = date_object[2]
                        value = datetime.date(int(year), int(month), int(day))
                    if key in keys:
                        keys[key] |= Q(**{key: value})
                    else:
                        keys[key] = Q(**{key: value})

            # generate final queryset filter
            if keys:
                final = None
                for key in keys:
                    if final:
                        final &= keys[key]
                    else:
                        final = keys[key]
                return queryset.filter(final)

        return queryset

    def filter_queryset(self, request, queryset, view):
        filtering = request.query_params.get('filtering')
        try:
            return CustomFilter.get_filtered_queryset(queryset, filtering)
        except FieldError as e:
            raise APIBadRequest(detail=e)
