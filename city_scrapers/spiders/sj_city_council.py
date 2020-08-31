import re
from datetime import datetime, timedeltas

from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class SjCityCouncilSpider(CityScrapersSpider):
    name = "sj_city_council"
    agency = "SJ City Council"
    timezone = 'America/Los_Angeles'
    start_urls = ["https://sanjose.granicus.com/ViewPublisher.php?view_id=51"]

    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.xpath('//div[@class="archive"]/table[@class="listingTable"]/tbody/tr[@class="odd"or@class="even"]'):
            print("steven testing")
            meeting = Meeting(
                title='testing123',
                description=self._parse_description(item),
                classification=self._parse_classification(item),
                start=self._parse_start(item),
                end=self._parse_end(item),
                all_day=self._parse_all_day(item),
                time_notes=self._parse_time_notes(item),
                location=self._parse_location(item),
                links=self._parse_links(item),
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting
        yield "Steven says hi"

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        title = item.xpath('//td[@headers="EventName"]//text()').extract()
        return title.extract()

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        date = item.xpath('//td[contains(@headers, "EventDate")]//text()')
        pattern = re.compile('([0]+[1-9]+|[1]+[0-2]+)\/([0]+[1-9]|[1-2]+[0-9]+|[3]+[0-1]+)\/([0-9]+[0-9]+)')
        date_groups = pattern.match(date)
        # add check if todo if date_groups doesn't work
        month, day, year = date_groups.groups()
        time = item.xpath('//td[contains(@headers, "EventTime")]//text()')
        pattern = re.compile('([1-9]+|[1]+[0-2]+)([0-6]+[0-9]+) (am|pm)')
        time_groups = pattern.match(time)
        hour, minutes, time_of_day = time_groups.groups()
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        date = item.xpath('//td[contains(@headers, "EventDate")]//text()')
        pattern = re.compile('([0]{1}[1-9]{1}|[1]{1}[0-2]{1})\/([0]{1}[1-9]|[1-2]{1}[0-9]{1}|[3]{1}[0-1]{1})\/([0-9]{1}[0-9]{1})')
        date_groups = pattern.match(date)
        # add check if todo if date_groups doesn't work
        month, day, year = map(int, date_groups.groups())
        date_str = date_groups.group(0)
        time = item.xpath('//td[contains(@headers, "EventTime")]//text()')
        pattern = re.compile('^\s*(([1-9]{1}|1[0-2]{1}):[0-6]{1}[0-9]{1}\s[ap]{1}m)\s*$')
        time_groups = pattern.match(time)
        # hour, minute, time_of_day = list(map(int, time_groups.groups()[0:2])) + [time_groups.group(3)]
        time_str = ' ' + time_groups.group(1)
        # if time_of_day == 'pm':
        #     hour *= 2
        return datetime.strptime(date_str + time_str, '%m/%d/%y %I:%M %p')

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        return {
            "address": "",
            "name": "",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": "", "title": ""}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
