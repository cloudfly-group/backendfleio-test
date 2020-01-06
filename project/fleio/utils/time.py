import datetime
import iso8601
import six


def parse_isotime(time_string):
    """Parse time from ISO 8601 format."""
    if type(time_string) is datetime.datetime:
        return time_string
    try:
        return iso8601.parse_date(time_string)
    except iso8601.ParseError as e:
        raise ValueError(six.text_type(e))
    except TypeError as e:
        raise ValueError(six.text_type(e))
