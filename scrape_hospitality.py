"""
To use call add_hours()
Right now this will just print json to console
"""

from enum import Enum
from lxml import html
import requests

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
    Enum of dining locations on Brandeis campus
    Each item has a tuple that contains the official title, geographic location, and link for that item.
    Do not access these by indexing the tuple. Instead, call title(), geo(), or link()
    """
    # dining locations with their own page
    USDAN = ('Usdan Kitchen', LOWER_USDAN, "https://www.brandeishospitality.com/locations/lower-usdan/?date=")
    SHERMAN = ('Farm Table at Sherman', SHERMAN_HASS, "https://www.brandeishospitality.com/locations/the-farm-table-at-sherman-2/?date=")
    KOSHER = ('Kosher Table at Sherman', SHERMAN_HASS, "https://www.brandeishospitality.com/locations/the-farm-table-at-sherman/?date=")
    STEIN = ('The Stein', SHERMAN_HASS, "https://www.brandeishospitality.com/locations/the-stein/?date=")
    UPPER = ('the Hive Culinary Studio', UPPER_USDAN, "https://www.brandeishospitality.com/locations/greens-grains/?date=")
    LOUIS = ("Louis' Deli", UPPER_USDAN, "https://www.brandeishospitality.com/locations/louis-deli/?date=")
    # uncomment to have Faculty Club hours added to the database
    # FACULTY = ('The Faculty Club', "https://www.brandeishospitality.com/locations/the-faculty-club/")

    # dining locations without their own page
    CSTORE = ('The Hoot', LOWER_USDAN, MENU_AND_HOURS)
    EINSTEIN = ('Einstein Bros. Bagels', SCC, MENU_AND_HOURS)
    STARBUCKS = ('Starbucks', FARBER, MENU_AND_HOURS)
    DUNKIN = ("Dunkin'", UPPER_USDAN, MENU_AND_HOURS)

    # TODO: add IBS dining options

    @staticmethod
    def title(location: 'DiningLocations') -> str:
        """
        :param location: from DiningLocations
        :return: formal title of the DiningLocation
        """
        return location.value[0]

    @staticmethod
    def geo(location: 'DiningLocations') -> str:
        """
        :param location: from DiningLocations
        :return: geographic location of given DiningLocation
        """
        return location.value[1]

    @staticmethod
    def link(location: 'DiningLocations') -> str:
        """
        :param location: from DiningLocations
        :return: link to given DiningLocation's page. if it doesn't have a page, MENU_AND_HOURS
        """
        return location.value[2]

    @staticmethod
    def no_page() -> tuple:
        """
        # get tuple of the locations that don't have an hours page
        :return:
        """
        return DiningLocations.CSTORE, DiningLocations.EINSTEIN, DiningLocations.STARBUCKS, DiningLocations.DUNKIN


def add_hours(date:str = "") -> bool:
    """
    add today's hours to the database as json
    :param date: optional parameter to add hours for specified date in format yyyy-mm-dd. default is today.
    :return: True if all hours were successfully written to the database, else False
    """
    # make a get request to statically load the Menu and Hours page
    response = requests.get(MENU_AND_HOURS + date)

    # check that the get request was successful or else handle the error
    # if the error could not be handled, halt execution
    if not handle_get_error(response):
        return False

    # create a tree for searching elements by lxml.xpath()
    tree = html.fromstring(response.content)

    # dictionary that keys dining location titles to a (start, end) tuple
    start_end = {}

    # add the start and end time for each location to the dictionary
    for element in tree.xpath('//tr[@class="row location"]'):
        # get the title of the dining location
        title = element.xpath('.//*[@class="open-now-location-link"]/text()')[0]
        # times are listed under these elements for each meal, so the start is just the first one
        start = element.xpath('.//span[@class="hour open_at"]/text()')[0]
        # times are listed under these elements for each meal, so the end time is just the last one
        end = element.xpath('.//span[@class="hour close_at"]/text()')[-1]
        # add the (start, end) tuple to the start_end dictionary
        start_end[title] = (start, end)

    # indicate in the dictionary which locations don't have hours today
    for location in DiningLocations:
        if DiningLocations.title(location) not in start_end:
            start_end[DiningLocations.title(location)] = (NO_START, NO_END)

    # create json for each location and add it to the database
    for location in DiningLocations:
        if not write_to_database(make_json(location, start_end[DiningLocations.title(location)], date)):
            return False

    return True


def make_json(location, start_end_tuple, date="") -> str:
    """
    :param location:
    :param start_end_tuple: tuple with start time at first index, end time at last index
    :param date: optional date to add to link in format yyyy-mm-dd
    :return: json string with info for the given location
    e.g.
    {The Stein: {
    "location: "SHERMAN-HASSENFELD"
    "start: "5:00 pm"
    "end: "12:00 am"
    "link: https://www.brandeishospitality.com/locations/the-stein/?date="
    }
    }
    """
    return ('{' + DiningLocations.title(location) + ': {\n' +
            '"location: "' + DiningLocations.geo(location) + '"\n' +
            '"start: "' + start_end_tuple[0] + '"\n' +
            '"end: "' + start_end_tuple[-1] + '"\n' +
            '"link: ' + DiningLocations.link(location) + date + '"\n' +
            '}\n' +
            '}')


def write_to_database(database_text: str) -> bool:
    """
    Write each json item in the given list to the database.
    Not fully implemented, just prints to console
    :return:
    """
    print(database_text)
    return True
    return False
    raise NotImplementedError


def handle_get_error(response: requests.Response) -> bool:
    """
    unimplemented method to handle response errors.
    :param response:
    :return:
    """
    # TODO: implement error handling
    return True
