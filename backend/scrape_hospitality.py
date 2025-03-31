"""
To use call add_hours()
Now it returns json data rather than printing to console
"""

from enum import Enum
from lxml import html
import requests
import json

# constants used when a dining location is not open today
NO_START = "##:##"
NO_END = "##:##"

# link to main Menu and Hours page
MENU_AND_HOURS = "https://www.brandeishospitality.com/menu-hours/?date="

# geographical locations that dining locations can be at
LOWER_USDAN = "LOWER USDAN (USDAN STUDENT CENTER)"
UPPER_USDAN = "UPPER USDAN (USDAN STUDENT CENTER)"
FARBER = "FARBER LIBRARY"
SHERMAN_HASS = "SHERMAN-HASSENFELD"
SCC = "SHAPIRO CAMPUS CENTER"
FACULTY_CENTER = "FACULTY CENTER"

class DiningLocations(Enum):
    """
    Enum of dining locations on Brandeis campus.
    Each item has a tuple that contains the official title, geographic location, and link for that item.
    Use the provided static methods to access title, geo, or link.
    """
    # dining locations with their own page
    USDAN = ('Usdan Kitchen', LOWER_USDAN, "https://www.brandeishospitality.com/locations/lower-usdan/?date=")
    SHERMAN = ('Farm Table at Sherman', SHERMAN_HASS, "https://www.brandeishospitality.com/locations/the-farm-table-at-sherman-2/?date=")
    KOSHER = ('Kosher Table at Sherman', SHERMAN_HASS, "https://www.brandeishospitality.com/locations/the-farm-table-at-sherman/?date=")
    STEIN = ('The Stein', SHERMAN_HASS, "https://www.brandeishhospitality.com/locations/the-stein/?date=")
    UPPER = ('the Hive Culinary Studio', UPPER_USDAN, "https://www.brandeishhospitality.com/locations/greens-grains/?date=")
    LOUIS = ("Louis' Deli", UPPER_USDAN, "https://www.brandeishhospitality.com/locations/louis-deli/?date=")
    # dining locations without their own page
    CSTORE = ('The Hoot', LOWER_USDAN, MENU_AND_HOURS)
    EINSTEIN = ('Einstein Bros. Bagels', SCC, MENU_AND_HOURS)
    STARBUCKS = ('Starbucks', FARBER, MENU_AND_HOURS)
    DUNKIN = ("Dunkin'", UPPER_USDAN, MENU_AND_HOURS)

    @staticmethod
    def title(location: 'DiningLocations') -> str:
        return location.value[0]

    @staticmethod
    def geo(location: 'DiningLocations') -> str:
        return location.value[1]

    @staticmethod
    def link(location: 'DiningLocations') -> str:
        return location.value[2]

    @staticmethod
    def no_page() -> tuple:
        return DiningLocations.CSTORE, DiningLocations.EINSTEIN, DiningLocations.STARBUCKS, DiningLocations.DUNKIN

def add_hours(date: str = "") -> str:
    """
    Add today's hours and return a JSON string with the data.
    :param date: optional parameter to add hours for specified date (yyyy-mm-dd).
    """
    response = requests.get(MENU_AND_HOURS + date)
    if not handle_get_error(response):
        return json.dumps({"error": "Failed to retrieve hours"})

    tree = html.fromstring(response.content)
    start_end = {}

    for element in tree.xpath('//tr[@class="row location"]'):
        title = element.xpath('.//*[@class="open-now-location-link"]/text()')[0]
        start = element.xpath('.//span[@class="hour open_at"]/text()')[0]
        end = element.xpath('.//span[@class="hour close_at"]/text()')[-1]
        start_end[title] = (start, end)

    for location in DiningLocations:
        if DiningLocations.title(location) not in start_end:
            start_end[DiningLocations.title(location)] = (NO_START, NO_END)

    results = []
    for location in DiningLocations:
        results.append(make_json(location, start_end[DiningLocations.title(location)], date))
        # Optionally, call write_to_database(json_data) if needed.
        write_to_database(results[-1])
    return json.dumps(results, indent=2, ensure_ascii=False)

def make_json(location, start_end_tuple, date="") -> dict:
    """
    Create a dictionary with info for the given location.
    """
    return {
        DiningLocations.title(location): {
            "location": DiningLocations.geo(location),
            "start": start_end_tuple[0],
            "end": start_end_tuple[-1],
            "link": DiningLocations.link(location) + date
        }
    }

def write_to_database(database_data: dict) -> bool:
    """
    Simulate writing JSON data to the database.
    (Currently, does nothing.)
    """
    # ...existing code...
    return True

def handle_get_error(response: requests.Response) -> bool:
    """
    Handle errors from the get request.
    """
    # TODO: implement proper error handling if needed
    return True

if __name__ == "__main__":
    # for testing purposes, print the JSON result
    print(add_hours(""))
