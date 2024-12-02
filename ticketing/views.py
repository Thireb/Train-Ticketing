from django.shortcuts import render
from datetime import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder

"""
CTA Ticketing System Views
This module handles the core ticketing functionality including zone management,
fare calculations, and ticket generation.
"""

# Station and zone mapping structure
# Format: zone -> main_station -> [connected_stations]
zone_map = {
    "Central": {
        "Centrala": [
            "Rede",
            "Ninia",
            "Bylyn",
            "Frestin",
            "Lomil",
            "Yaen",
            "Jaund",
            "Tallan",
        ],
        "Frestin": ["Soth"],
    },
    "Midtown": {
        "Yaen": ["Quthiel", "Wicyt"],
        "Jaund": ["Riladia"],
        "Tallan": ["Oloadus"],
        "Ninia": ["Sylas"],
        "Lomil": ["Garion"],
        "Garion": ["Ralith"],
        "Soth": ["Obelyn"],
        "Bylyn": ["Agralle"],
        "Agralle": ["Docia", "Stonyam"],
        "Rede": ["Riclya"],
    },
    "Downtown": {
        "Riclya": ["Brunad"],
        "Brunad": ["Erean"],
        "Quthiel": ["Zord"],
        "Riladia": ["Perinad"],
        "Oloadus": ["Keivia"],
        "Sylas": ["Elyot"],
        "Elyot": ["Adohad"],
        "Ralith": ["Holmer"],
        "Holmer": ["Vertwall"],
        "Vertwall": ["Ruril"],
        "Obelyn": ["Ederif"],
        "Stonyam": ["Ryall"],
        "Ryall": ["Pryn"],
        "Docia": ["Marend"],
    }
}

# Flat list of stations in each zone for quick lookups
stations_in_zones = {
    "Central": [
        "Centrala",
        "Rede",
        "Ninia",
        "Bylyn",
        "Frestin",
        "Lomil",
        "Yaen",
        "Jaund",
        "Tallan",
        "Soth",
    ],
    "Midtown": [
        "Quthiel",
        "Wicyt",
        "Riladia",
        "Oloadus",
        "Sylas",
        "Garion",
        "Ralith",
        "Obelyn",
        "Agralle",
        "Docia",
        "Stonyam",
        "Riclya",
    ],
    "Downtown": [
        "Brunad",
        "Erean",
        "Zord",
        "Perinad",
        "Keivia",
        "Elyot",
        "Adohad",
        "Holmer",
        "Vertwall",
        "Ruril",
        "Ederif",
        "Ryall",
        "Pryn",
        "Marend",
    ],
}


def get_station_zone(station_name):
    """Find which zone a station belongs to"""
    for zone, stations in stations_in_zones.items():
        if station_name in stations:
            return zone
    return None


FARES = {
    'adult': 2105,    # cents per zone
    'child': 1410,    # cents per zone
    'senior': 1025,   # cents per zone
    'student': 1750,  # cents per zone
}

def get_station_zone(station_name):
    """Find which zone a station belongs to"""
    for zone, areas in zone_map.items():
        # Check main stations
        if station_name in areas:
            return zone
        # Check connected stations
        for main_station, connected in areas.items():
            if station_name in connected:
                return zone
    return None

def calculate_zones_traveled(start_station: str, end_station: str) -> int:
    """
    Calculate the number of zones traveled between two stations.
    
    The calculation follows these rules:
    1. Same zone = 1 zone
    2. Adjacent zones = 2 zones
    3. Crossing multiple zones = actual zones crossed
    
    Args:
        start_station (str): Name of departure station
        end_station (str): Name of destination station
        
    Returns:
        int: Number of zones traveled (minimum 1)
        
    Example:
        >>> calculate_zones_traveled("Centrala", "Zord")
        3  # Crosses Central -> Midtown -> Downtown
    """
    zone_order = ['Central', 'Midtown', 'Downtown']
    start_zone = get_station_zone(start_station)
    end_zone = get_station_zone(end_station)
    start_idx = zone_order.index(start_zone)
    end_idx = zone_order.index(end_zone)
    return abs(end_idx - start_idx) + 1

def calculate_fare(num_zones: int, num_travelers: dict) -> dict:
    """
    Calculate total fare based on zones traveled and traveler types.
    
    Args:
        num_zones (int): Number of zones the journey covers
        num_travelers (dict): Count of each type of traveler
            Format: {'adult': n, 'child': m, 'senior': p, 'student': q}
            
    Returns:
        dict: Detailed fare breakdown including:
            - Per category costs
            - Total number of travelers
            - Total fare in cents
            
    Example:
        >>> calculate_fare(2, {'adult': 1, 'child': 1})
        {
            'breakdown': {
                'adult': {'count': 1, 'fare_per_zone': 2105, 'total': 4210},
                'child': {'count': 1, 'fare_per_zone': 1410, 'total': 2820}
            },
            'total_travelers': 2,
            'total_fare': 7030
        }
    """
    results = {
        'breakdown': {},
        'total_travelers': 0,
        'total_fare': 0
    }
    
    for category, count in num_travelers.items():
        if count > 0:
            fare_per_zone = FARES[category]
            total = count * fare_per_zone * num_zones
            results['breakdown'][category] = {
                'count': count,
                'fare_per_zone': fare_per_zone,
                'total': total
            }
            results['total_travelers'] += count
            results['total_fare'] += total
    
    return results

def index(request):
    """
    Main view for the ticketing system.
    
    Handles both GET and POST requests:
    - GET: Displays the ticket booking form
    - POST: Processes ticket requests and displays fare calculation
    
    Context includes:
    - Zone and station information
    - Fare calculations (for POST requests)
    - Ticket details (for POST requests)
    
    Template: index.html
    """
    context = {
        'zone_map': zone_map,
        'stations_in_zones': stations_in_zones,
    }
    
    if request.method == 'POST':
        # Extract journey details from form
        start_station = request.POST.get('start_station')
        end_station = request.POST.get('end_station')
        travelers = {
            'adult': int(request.POST.get('adult', 0)),
            'child': int(request.POST.get('child', 0)),
            'senior': int(request.POST.get('senior', 0)),
            'student': int(request.POST.get('student', 0))
        }
        
        # Calculate journey details
        start_zone = get_station_zone(start_station)
        end_zone = get_station_zone(end_station)
        zones_traveled = calculate_zones_traveled(start_station, end_station)
        
        # Calculate fare and update context
        fare_details = calculate_fare(zones_traveled, travelers)
        
        context.update({
            'ticket_time': datetime.now(),
            'start_station': start_station,
            'end_station': end_station,
            'start_zone': start_zone,
            'end_zone': end_zone,
            'zones_traveled': zones_traveled,
            'fare_details': fare_details
        })
    
    return render(request, 'index.html', context)
