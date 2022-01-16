from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Course:
    name: str
    grade: float


@dataclass
class ExtraCurricular:
    name: str
    type: str
    hours: float


@dataclass
class UserData:
    courses: List[Course]
    extra_curriculars: List[ExtraCurricular]
    want_coop: bool = False
    program_of_choice: str = 'Mathematics'
    is_ap: bool = False
    is_ib: bool = False
    is_esl: bool = False
    location: Optional[str] = None
    are_international: bool = False


@dataclass
class ScrapingData:
    program_name: str = 'NULL'
    province: str = 'NULL'
    school_name: str = 'NULL'
    ouac_code: str = 'NULL'
    degrees: Optional[List[str]] = None
    coop_option: bool = False
    req_courses: Optional[List[str]] = None
    admission_range: str = "NULL"
    enrolment: int = 0


@dataclass
class ReturnData:
    entrance_chance: str = 'LOW CHANCE'
    reviews: Optional[List[str]] = None


@dataclass
class Program:
    name: str = 'NULL'
    link: str = 'NULL'
    information: Optional[ScrapingData] = None

    def __dict__(self):
        return {'name': self.name, 'link': self.link,
                'information': self.information.__dict__}
