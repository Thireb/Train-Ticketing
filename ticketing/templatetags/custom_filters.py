from django import template

register = template.Library()

@register.filter
def get(dictionary, key):
    """Get value from dictionary using key in template"""
    if isinstance(dictionary, dict):
        return dictionary.get(key, '')
    return ''

@register.filter
def get_station_zone(station_name, stations_in_zones):
    """Get the zone name for a given station"""
    for zone, stations in stations_in_zones.items():
        if station_name in stations:
            return zone
    return ''
