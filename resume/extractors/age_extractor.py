import re


class AgeExtractor:
    __PATTERN_AGE = re.compile(r'(?<![\wа-яА-Я])'
                               r'(\d{2}\s{1,3}(?:лет|год|года)|'
                               r'возраст[^\d]{1,3}\d{2})'
                               r'(?![\wа-яА-Я])')
    __PATTERN_EXPERIENCE = re.compile(r'опыт работы[^\d]{1,3}\d{2}[^\d]{1,3}(?:лет|год|года)')
    __PATTERN_NUMBER = re.compile(r'\d{2}')
    __MIN_AGE = 14

    def __extract_experiences(self, text):
        return [int(self.__PATTERN_NUMBER.search(match).group(0)) for match in self.__PATTERN_EXPERIENCE.findall(text)]

    def __extract_ages(self, text):
        ages = [int(self.__PATTERN_NUMBER.search(match).group(0)) for match in self.__PATTERN_AGE.findall(text)]
        return list(filter(lambda x: x >= self.__MIN_AGE, ages))

    def get_info(self, text):
        text = text.replace('\n', ' ').lower()
        ages = self.__extract_ages(text)
        exp = self.__extract_experiences(text)
        if exp:
            ages = list(filter(lambda x: x not in exp, ages))
        return ages[0] if ages else None
