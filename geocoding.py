import requests

GEOCODE_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'
FIND_PLACE_API_URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'
API_KEY='YOUR_API_KEY'

def geocoding(address, API_KEY=API_KEY, GEOCODE_API_URL=GEOCODE_API_URL):
    """Geocode a location based on address details.

    Args:
        address (str): Details of a location such as country, city, postcode
            or street name.
        API_KEY (str): Key for the Google API.
        GEOCODE_API_URL (str): Endpoint for the Google Geocode API.

    Returns:
        geodata (dict): Geocoded information for the most relevant result to
            the given address.

    """
    # define the parameters of the search
    params = {
    'address': '{}'.format(address),
    'key': API_KEY
    }

    # Do the request and get the response data
    response = requests.get(GEOCODE_API_URL, params=params)
    response = response.json()

    geodata = parse_response(response)
    return geodata

def reverse_geocoding(lat, lng, API_KEY=API_KEY, GEOCODE_API_URL=GEOCODE_API_URL):
    """Reverse geocode a location based on its latitude and longitude.

    Args:
        lat (float): Latitude.
        lon (float): Longitude.

    Returns:
        geodata (dict): Geocoded information for the most relevant result to
            the given longitude and latitude.

    """
    params = {
    'latlng': '{},{}'.format(lat, lng),
    'key': API_KEY
    }

    # Do the request and get the response data
    response = requests.get(GEOCODE_API_URL, params=params)
    response = response.json()
    geodata = parse_response(response)
    return geodata

def place_by_name(place, API_KEY=API_KEY, FIND_PLACE_API_URL=FIND_PLACE_API_URL):
    """Geocode a location by searching with its name.

    Args:
        place (str): Name of the place. It can be a restaurant, bar, monuement,
            whatever you would normally search in Google Maps.
        API_KEY (str): Key for the Google API.
        FIND_PLACE_API_URL (str): Endpoint for the Google Places API.
    Returns:

    """
    params = {
        'input': '{}'.format(place),
        'fields':'name,geometry,formatted_address',
        'inputtype':'textquery',
        'key': API_KEY
        }

    # Do the request and get the response data
    response = requests.get(FIND_PLACE_API_URL, params=params)

    response = response.json()['candidates'][0]

    geodata = dict()
    geodata['lat'] = response['geometry']['location']['lat']
    geodata['lng'] = response['geometry']['location']['lng']
    geodata['address'] = response['formatted_address']

    return geodata

def check_status(response):
    """Check if the server successfully answered the HTTP request.

    Args:
        response (Requests obj): Response of a request.

    Returns:
        True, if the status code is 200.

    """
    if response.status_code == 200:
        return True

def parse_response(response):
    """Parse spatial details from a JSON object.

    Args:
        response (Requests obj): Response of a request.

    Returns:
        geodata (dict): Geocoded information for the most relevant result to
            the given longitude and latitude.

    """
    # Use the first result
    res = response['results'][0]

    # Store attributes
    geodata = dict()
    geodata['lat'] = res['geometry']['location']['lat']
    geodata['lng'] = res['geometry']['location']['lng']
    geodata['address'] = res['formatted_address']

    for output in res['address_components']:
        if output['types'][0] == 'postal_town':
            geodata['postal_town'] = output['long_name']
        elif output['types'][0] == 'administrative_area_level_2':
            geodata['administrative_area_level_2'] = output['long_name']
        elif output['types'][0] == 'administrative_area_level_1':
            geodata['administrative_area_level_1'] = output['long_name']
        elif output['types'][0] == 'country':
            geodata['country'] = output['long_name']
        elif output['types'][0] == 'route':
            geodata['route'] = output['long_name']
        else:
            continue

    return geodata

def main():
    """Run some examples."""

    # Search for places
    places = ['Look mum no hands!', 'O2 Arena']
    geocoded_places = {place:place_by_name(place=place) for place in places}
    print('Geocoded places:\n{}'.format(geocoded_places))

    # Geocode locations
    locations = ['GR Athens', 'UK London']
    geocoded_locations = {loc:geocoding(address=loc) for loc in locations}
    print('Geocoded places:\n{}'.format(geocoded_locations))

    # Reverse geocode locations
    latlon = [(49.57152, 11.21482), (51.524061, -0.096149)]
    r_geocoded_locations = {loc:reverse_geocoding(lat=loc[0], lng=loc[1])
                            for loc in latlon}
    print('Geocoded places:\n{}'.format(r_geocoded_locations))

if __name__ == '__main__':
    main()
