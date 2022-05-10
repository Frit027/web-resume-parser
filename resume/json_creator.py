import json
from .extractors.education_extractor import EducationExtractor
from .extractors.name_extractor import NameExtractor
from .extractors.contact_info_extractor import ContactInfoExtractor
from .extractors.age_extractor import AgeExtractor
from .extractors.skills_extractor import SkillsExtractor
from .extractors.experience_extractor import ExperienceExtractor


class JSONCreator:
    def __init__(self):
        self.__education_extractor = EducationExtractor()
        self.__name_extractor = NameExtractor()
        self.__age_extractor = AgeExtractor()
        self.__contact_info_extractor = ContactInfoExtractor()
        self.__skills_extractor = SkillsExtractor()
        self.__experience_extractor = ExperienceExtractor()

    def __get_data(self, resume_text):
        email, phone = self.__contact_info_extractor.get_info(resume_text)
        return {
            'name': self.__name_extractor.get_info(resume_text),
            'age': self.__age_extractor.get_info(resume_text),
            'email': email,
            'phone': phone,
            'education': self.__education_extractor.get_info(resume_text),
            'experience': self.__experience_extractor.get_info(resume_text),
            'skills': self.__skills_extractor.get_info(resume_text)
        }

    def get_json(self, resume_text):
        return json.dumps(self.__get_data(resume_text), indent=4, ensure_ascii=False).encode('utf-8')
