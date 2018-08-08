from elife_bus_sdk.events import Event


class DigestEvent(Event):
    _type = 'digest'
    required_fields = ['id']