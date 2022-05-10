import re
from string import ascii_letters
from ..models import (ProgramLang, SkillWithSlash, OperatingSystem, MarkupLang,
                      StylesheetLang, VersionControl, DB, IOS, Android, ML,
                      GameDev, Testing, SysAdmin, DevOps, Frontend, Backend)


class SkillsExtractor:
    __PATTERN_SKILL = re.compile(r'[a-zA-Zéöá\d./+*#@:′!-]+(?![а-яА-Я])(?: [a-zA-Zéöá\d./+*#@:′!-]+)*')
    __PATTERN_DRIVING = re.compile(r'водительск(их|ие)|права категории')
    __PATTERN_DRIVING_CATEGORY = re.compile(r'[bcd]')
    __START_WRONG_CHARACTERS = ('.', ':', '-', '+', '/')
    __END_WRONG_CHARACTERS = ('.', ':', '-', '/')

    def __init__(self):
        self.program_languages = ProgramLang.get_all()
        self.skills_with_slash = SkillWithSlash.get_all()
        self.operating_systems = OperatingSystem.get_all()
        self.markup_languages = MarkupLang.get_all()
        self.stylesheet_languages = StylesheetLang.get_all()
        self.version_control = VersionControl.get_all()
        self.databases = DB.get_all()
        self.ios = IOS.get_all()
        self.android = Android.get_all()
        self.ml = ML.get_all()
        self.gamedev = GameDev.get_all()
        self.testing = Testing.get_all()
        self.sys_admin = SysAdmin.get_all()
        self.dev_ops = DevOps.get_all()
        self.frontend = Frontend.get_all()
        self.backend = Backend.get_all()

    def __get_driving_categories(self, text):
        match = self.__PATTERN_DRIVING.search(text)
        if match:
            word = match.group(0)
            i = text.find(word) + len(word)
            return self.__PATTERN_DRIVING_CATEGORY.findall(text[i:])
        return []

    def __remove_driving_categories(self, text, skills):
        [skills.remove(category.upper()) for category in self.__get_driving_categories(text)
         if category.upper() in skills]

    def __filter_words(self, words):
        return list(filter(lambda x:
                           any(c in x for c in ascii_letters)
                           and not x.isdigit()
                           and '://' not in x and 'www' not in x
                           and all(c != x for c in self.__START_WRONG_CHARACTERS),
                           words))

    def __remove_wrong_characters(self, words):
        words = list(map(lambda x: x[:-1] if x[-1] in self.__END_WRONG_CHARACTERS else x, words))
        return list(map(lambda x: x[1:] if x[0] in self.__START_WRONG_CHARACTERS else x, words))

    def __split_words_with_slash(self, words):
        skills = []
        for skill in words:
            if '/' in skill and skill.lower() not in self.skills_with_slash:
                for word in skill.split('/'):
                    skills.append(word.strip())
            else:
                skills.append(skill.strip())
        return skills

    @staticmethod
    def __get_filtered_skills(skills, technology_lst):
        return list(set(skill.lower() for skill in skills if skill.lower() in technology_lst))

    def get_info(self, text):
        skills = self.__filter_words(self.__PATTERN_SKILL.findall(text))
        skills = self.__remove_wrong_characters(skills)
        skills = self.__split_words_with_slash(skills)
        self.__remove_driving_categories(text.lower(), skills)
        return {
            'program_lang': self.__get_filtered_skills(skills, self.program_languages),
            'stylesheet_lang': self.__get_filtered_skills(skills, self.stylesheet_languages),
            'markup_lang': self.__get_filtered_skills(skills, self.markup_languages),
            'db': self.__get_filtered_skills(skills, self.databases),
            'operating_system': self.__get_filtered_skills(skills, self.operating_systems),
            'version_control': self.__get_filtered_skills(skills, self.version_control),
            'ios': self.__get_filtered_skills(skills, self.ios),
            'android': self.__get_filtered_skills(skills, self.android),
            'ml': self.__get_filtered_skills(skills, self.ml),
            'gamedev': self.__get_filtered_skills(skills, self.gamedev),
            'testing': self.__get_filtered_skills(skills, self.testing),
            'sys_admin': self.__get_filtered_skills(skills, self.sys_admin),
            'devops': self.__get_filtered_skills(skills, self.dev_ops),
            'frontend': self.__get_filtered_skills(skills, self.frontend),
            'backend': self.__get_filtered_skills(skills, self.backend)
        }
