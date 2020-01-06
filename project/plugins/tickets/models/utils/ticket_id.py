import random
import string
from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from django.apps import apps
from django.conf import settings
from django.db.utils import OperationalError
from django.db.utils import ProgrammingError
from django.utils.deconstruct import deconstructible

from fleio.core.utils import is_valid_ascii


@deconstructible
class TicketId:
    # NOTE(manu): redundant class, delete this when squashing migrations
    def __init__(self, model_name):
        self.model_name = model_name

    def __call__(self):
        random.seed()
        model_class = apps.get_model(self.model_name)
        utc_now = datetime.utcnow()

        while True:
            ticket_id_base = 'T-{}{:02}{:02}-{:02}{:02}-'.format(
                utc_now.year % 100,
                utc_now.month,
                utc_now.day,
                utc_now.hour,
                utc_now.min
            )
            ticket_id_suffix = random.randint(0, 100000)
            ticket_id = ticket_id_base + '{:05}'.format(ticket_id_suffix)
            try:
                model_class.objects.get(id=ticket_id)
            except model_class.DoesNotExist:
                break
            except (ProgrammingError, OperationalError):
                # db table probably doesn't exist yet
                # workaround for the fact that schema migration (uselessly) tries to get the field's default value
                # ProgrammingError - for mysql
                # OperationalError - for sqlite
                return None
        return ticket_id


class TicketIdOptionsGenerator:
    MARKER = '%'
    FULL_YEAR = '%Y'
    YEAR = '%y'
    MONTH = '%M'
    MINUTE = '%m'
    DAY = '%D'
    HOUR = '%h'
    RANDOM_NUMBER = '%n'
    RANDOM_UPPERCASE_LETTER = '%L'
    RANDOM_LOWERCASE_LETTER = '%l'

    forbidden_characters = (';', '/', '?', ':', '@', '=', '&', '<', '>', '#', '{', '}', '|', '^', '~', '[', ']', '`',
                            '\\',)  # reserved/unsafe characters that would need encoding in URL

    allowed_keys = ('Y', 'y', 'M', 'm', 'D', 'h', 'n', 'L', 'l')  # allowed keys to use after the "%" sign
    random_char_keys = ('L', 'l', 'n')  # keys that will get converted in random chars

    def __init__(self):
        self.now = datetime.utcnow()

    def get_full_year(self):
        """year in full format (e.g. 2019)"""
        return str(self.now.year)

    def get_year(self):
        """year in small format (e.g. 19)"""
        return str(self.now.year)[2:]

    def get_minute(self):
        minute = str(self.now.minute)
        if len(minute) == 1:
            return '0{}'.format(minute)
        return minute

    def get_hour(self):
        return str(self.now.hour)

    def get_month(self):
        month = str(self.now.month)
        if len(month) == 1:
            return '0{}'.format(month)
        return month

    def get_day(self):
        day = str(self.now.day)
        if len(day) == 1:
            return '0{}'.format(day)
        return day

    @staticmethod
    def get_random_number():
        return str(random.randint(0, 9))

    @staticmethod
    def get_random_lowercase_letter():
        return random.choice(string.ascii_lowercase)

    @staticmethod
    def get_random_uppercase_letter():
        return random.choice(string.ascii_uppercase)


def generate_ticket_id(id_format: str) -> str:
    ticket_id = id_format
    options_gen = TicketIdOptionsGenerator()  # type: TicketIdOptionsGenerator

    while options_gen.MARKER in ticket_id:
        ticket_id = ticket_id.replace(options_gen.YEAR, options_gen.get_year())
        ticket_id = ticket_id.replace(options_gen.MONTH, options_gen.get_month())
        ticket_id = ticket_id.replace(options_gen.DAY, options_gen.get_day())
        ticket_id = ticket_id.replace(options_gen.HOUR, options_gen.get_hour())
        ticket_id = ticket_id.replace(options_gen.MINUTE, options_gen.get_minute())
        ticket_id = ticket_id.replace(options_gen.FULL_YEAR, options_gen.get_full_year())
        ticket_id = ticket_id.replace(options_gen.RANDOM_NUMBER, options_gen.get_random_number(), 1)
        ticket_id = ticket_id.replace(options_gen.RANDOM_LOWERCASE_LETTER, options_gen.get_random_lowercase_letter(), 1)
        ticket_id = ticket_id.replace(options_gen.RANDOM_UPPERCASE_LETTER, options_gen.get_random_uppercase_letter(), 1)

    return ticket_id


def generate_ticket_id_regex(id_format: str):
    """Presumes that id_format is a valid one validated using the validate_ticket_id method"""
    options = TicketIdOptionsGenerator()  # type: TicketIdOptionsGenerator

    regex_format = id_format

    one_digit = r'\d'
    two_digits = r'\d\d'
    four_digits = r'\d\d\d\d'
    non_digit = r'\D'

    while options.MARKER in regex_format:
        regex_format = regex_format.replace(options.YEAR, two_digits)
        regex_format = regex_format.replace(options.MONTH, two_digits)
        regex_format = regex_format.replace(options.DAY, two_digits)
        regex_format = regex_format.replace(options.HOUR, two_digits)
        regex_format = regex_format.replace(options.MINUTE, two_digits)
        regex_format = regex_format.replace(options.FULL_YEAR, four_digits)
        regex_format = regex_format.replace(options.RANDOM_NUMBER, one_digit, 1)
        regex_format = regex_format.replace(options.RANDOM_LOWERCASE_LETTER, non_digit, 1)
        regex_format = regex_format.replace(options.RANDOM_UPPERCASE_LETTER, non_digit, 1)
    dynamic_regex = r'{}'.format(regex_format)
    final_regex = r'(\[#' + dynamic_regex + r'\])'
    return final_regex


def validate_ticket_id(id_format: str) -> (bool, str):
    """
    Validates the ticket id format to have only ascii chars, not have empty spaces, use only the allowed keys after
    the "%" sign and use a minimum number of random chars
    :param id_format: the id format as a string
    :return: returns a tuple containing the validation result as bool and the associated message
    """
    if not id_format:
        return False, _('A valid id format is required.')
    if is_valid_ascii(value=id_format) is False:
        return False, _('Non ASCII characters are not allowed for defining ID format')
    if ' ' in id_format:
        return False, _('Empty characters are not allowed!')
    if id_format[-1:] == TicketIdOptionsGenerator.MARKER:
        return False, _('Format cannot end in "{}"').format(TicketIdOptionsGenerator.MARKER)
    if id_format[0] in TicketIdOptionsGenerator.forbidden_characters:
        return False, _('Forbidden character "{}" used in the ticket id format.').format(id_format[0])
    i = 0
    min_random_chars = getattr(settings, 'TICKET_ID_MIN_RANDOM_CHARS', 6)
    random_chars = 0  # counter for random characters in ticket_id format
    while i < len(id_format) - 1:
        current_char = id_format[i]
        next_char = id_format[i + 1]
        if next_char in TicketIdOptionsGenerator.forbidden_characters:
            return False, _('Forbidden character "{}" used in the ticket id format.').format(next_char)
        if current_char == TicketIdOptionsGenerator.MARKER:
            if next_char not in TicketIdOptionsGenerator.allowed_keys:
                return False, _('Unrecognized key "{}" at position {} after the "{}" sign').format(
                    next_char, i + 1, TicketIdOptionsGenerator.MARKER
                )
            if next_char in TicketIdOptionsGenerator.random_char_keys:
                random_chars += 1
        i += 1
    if random_chars < min_random_chars:
        return False, _('You need to use at least {} random characters').format(str(min_random_chars))

    return True, _('Valid format')
