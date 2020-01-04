from fleio.utils.time import parse_isotime


def parse_dtime_without_microseconds(dt):
    """Some events have microseconds, others don't, for the same date/time in Kilo."""
    return parse_isotime(dt).replace(microsecond=0)


class Event:
    def __init__(self, event, overwrite_mappings=None):
        """Wraps a Ceilometer Event class.

        The overwrite_mappings param can overwrite event traits definition:
         - ex: {'created_at': 'datetime'}: if created_at is found in traits it will
           always be treated as a datetime.
        """
        self._event = event
        setattr(self._event, 'trait', Traits(self._event.traits, overwrite_mappings))

    def __getattr__(self, attr):
        if attr == 'generated':
            return parse_dtime_without_microseconds(self._event.generated)
        return self._event.__getattr__(attr)


class Traits:
    MAPPINGS = {'datetime': parse_dtime_without_microseconds,
                'float': float,
                'integer': int
                }

    def __init__(self, traits, overwrite_mappings=None):
        self._traits = traits
        self.overwrite_mappings = overwrite_mappings or dict()

    def __getattr__(self, attr):
        for trait in self._traits:
            if trait['name'] == attr:
                trait_type = self.overwrite_mappings.get(trait['name'], trait['type'])
                try:
                    if trait_type in self.MAPPINGS:
                        return self.MAPPINGS[trait_type](trait['value'])
                except ValueError:
                    return None
                return trait['value']
        raise AttributeError(attr)


class RawEvent:
    MAPPINGS = {'datetime': parse_dtime_without_microseconds,
                'float': float,
                'integer': int
                }

    def __init__(self, event_type, payload, metadata, keep_traits=None, overwrite_mappings=None, region=None):
        self.event_type = event_type
        self.payload = payload
        self.message_id = metadata.get('message_id', 'n/a')
        self.generated = metadata.get('timestamp', None)
        self.region = region
        if self.generated:
            self.generated = parse_dtime_without_microseconds(self.generated)
        traits = list()
        for attribute in payload:
            if keep_traits and attribute in keep_traits:
                if isinstance(payload[attribute], int):
                    traits.append({'name': attribute, 'type': 'integer', 'value': payload[attribute]})
                else:
                    traits.append({'name': attribute, 'type': 'string', 'value': payload[attribute]})
        # Add region as a trait
        traits.append({'name': 'region', 'type': 'string', 'value': self.region})

        self.traits = traits
        self.trait = Traits(self.traits, overwrite_mappings)
