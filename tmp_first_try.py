from typing import List, Tuple

from bs4 import BeautifulSoup
from pydantic import BaseModel

from base.classes import BaseWebScraper

"""
class SearchFields:
    KeyWords: Optional[List[str]] = ''
    SortBy: Enum = ''
    PaymentFrom: Optional[int] = ''

    Region: Enum = ''
    City: str = ''
    Subway: str = ''
    WorkSphere: Optional[Enum] = ''

    WorkingSchedule: Optional[List[Enum]] = ''
    Education: Optional[List[Enum]] = ''
    WorkExperience: Optional[List[Enum]] = ''
    Gender: Optional[Enum] = ''
    DoNotShow: Optional[List[Enum]] = ''
"""


class WorkPlace(BaseModel):
    PeriodsOfEmployment: Tuple[str, str] = ()
    Position: str = ""
    Company: str = ""
    Responsibilities: str = ""


class ParsingFields(BaseModel):
    Name: str = ""
    Accommodation: str = ""
    Salary: str = ""
    WorkSchedule: str = ""  # TODO make Set[Enum]
    EducationShort: str = ""  # TODO make Enum
    WorkExperience: str = ""
    Nationality: str = ""
    Gender: str = ""
    Age: str = ""


"""
class ParsingFields:
    ...
    Contacts = ...
    ...
    WorkExperienceDetailed: List[Education]
    EducationDetailed: List[Education]
    OtherInformation: ...


class WorkPlace(BaseModel):
    PeriodOfEmployment = ...
    Position = ...
    Company = ...
    Responsibilities = ...
    

class Education:
    Education: str = ...
    Graduation: str = ...
    School: str = ...
    Specialty: str = ...
"""


class JobLabScraper(BaseWebScraper):
    HOME_URL: str = 'https://joblab.ru/resume'  # TODO mace ABC param

    def fetch_page_source(self) -> str:
        self._driver.get(url=JobLabScraper.HOME_URL)
        return self._driver.page_source


class ContentParser:
    @staticmethod
    def parse_content(html: str) -> List[str]:
        soup: BeautifulSoup = BeautifulSoup(html=html, features='html.parser')
        return [element.text for element in soup.find_all(name='p')]


if __name__ == '__main__':
    with JobLabScraper() as scraper:
        page_source: str = scraper.fetch_page_source()
        content: List[str] = ContentParser.parse_content(html=page_source)
        print(content)
