import re
from dateparser import parse
from datetime import datetime


class ExperienceExtractor:
    __JOB_SECTION = 'опыт работы'
    __NOW_DATE_WORDS = ('продолжаю', 'наст')

    # опыт работы - 7 лет и 1 месяц, опыт работы — 2 года 11 месяцев, опыт работы - 7 месяцев
    __PATTERN_EXPERIENCE = re.compile(r'(?<=опыт работы)\D{1,5}\d{1,2} '
                                      r'(?:(?:лет|года|год) (?:и )?\d{1,2} (?:месяцев|месяца|месяц)|'
                                      r'(?:лет|года|год)|'
                                      r'(?:месяцев|месяца|месяц))')
    __PATTERN_INTERVAL_VARIANTS = (
        # 2004, февраль — 2006, апрель
        re.compile(r'\d{4}, [а-я]{3,8} — \d{4}, [а-я]{3,8}|\d{4}, [а-я]{3,8} — продолжаю работать'),
        # 01/2020 - 05/2021
        re.compile(r'\d{2}/\d{4} - \d{2}/\d{4}|\d{2}/\d{4} - наст\. время'),
        # май 2015 - апрель 2020
        re.compile(r'[а-я]{3,8} \d{4} - [а-я]{3,8} \d{4}|[а-я]{3,8} \d{4} - по настоящее время')
    )

    @staticmethod
    def __str_to_years(experience):
        match_year = re.search(r'\d{1,2}(?= [гл])', experience)
        match_month = re.search(r'\d{1,2}(?= м)', experience)
        year = int(match_year.group(0)) if match_year else 0
        month = int(match_month.group(0)) if match_month else 0
        return round((year * 12 + month) / 12, 1)

    def __intervals_to_years(self, lst):
        years = 0
        pattern = '01/{}' if '/' in lst[0] else '{} 1'
        for interval in lst:
            d1, d2 = list(
                map(lambda x:
                    parse(pattern.format(x.strip()), settings={'TIMEZONE': 'UTC'}, languages=['ru'])
                    if all(word not in x for word in self.__NOW_DATE_WORDS)
                    else parse(datetime.strptime(str(datetime.now()), '%Y-%d-%m %H:%M:%S.%f')
                                       .strftime('%Y-%m-%d %H:%M:%S'),
                               settings={'TIMEZONE': 'UTC'},
                               languages=['ru']),
                    interval.split('-'))
            )
            years += abs((d2 - d1).days)
        return round(years / (12 * 30), 1)

    def __is_has_experience(self, text):
        return text.find(self.__JOB_SECTION) != -1

    def __get_total_experience(self, text):
        return self.__PATTERN_EXPERIENCE.search(text)

    def __find_intervals(self, text):
        idx = text.find(self.__JOB_SECTION)
        lst = []
        for pattern in self.__PATTERN_INTERVAL_VARIANTS:
            lst = pattern.findall(text[idx:])
            if not lst:
                lst = pattern.findall(text[:idx])
            if lst:
                break
        return list(map(lambda x: x.replace('—', '-'), lst))

    def get_info(self, text):
        text = text.lower().replace('\n', ' ')
        experience = None
        if self.__is_has_experience(text):
            total_experience = self.__get_total_experience(text)
            if total_experience:
                experience = self.__str_to_years(total_experience.group(0).strip())
            else:
                intervals = self.__find_intervals(text)
                if intervals:
                    experience = self.__intervals_to_years(intervals)
        return experience
