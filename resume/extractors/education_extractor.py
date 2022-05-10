from natasha import Segmenter, NewsNERTagger, NewsEmbedding, Doc
from resume.utilities import remove_invalid_quotes, remove_invalid_brackets
import re


class EducationExtractor:
    __LEVELS = ('среднее специальное', 'среднее профессиональное', 'среднее неполное', 'средне-специальное', 'среднее',
                'два и более высших', 'второе высшее', 'неоконченное высшее', 'неполное высшее', 'высшее',
                'бакалавр', 'магистр', 'специалитет', 'магистратура', 'аспирантура', 'докторантура',
                'MBA', 'курсы переподготовки', 'учащийся школы', 'кандидат наук', 'доктор наук')
    __ACADEMIES = ('университет', 'институт', 'техникум', 'колледж', 'академия')
    __WRONG_ABBREVIATIONS = ('ООП', 'ОАО', 'ООО', 'ЗАО', 'АО', 'ОВМ', 'СССР')

    __PATTERN_LEVEL = re.compile('|'.join(__LEVELS))
    __PATTERN_SECTION = re.compile(r'Образование|Основное образование')
    __PATTERN_YEAR = re.compile(r'19[567890]\d|2\d{3}')
    __PATTERN_ABBREVIATION = re.compile(r'(?<![\wа-яА-Я])'
                                        r'("[А-Я]{3,5}"\s[А-Я]{3,5}|'
                                        r'[А-Я]{3,5}\s"[А-Я]{3,5}"|'
                                        r'[А-Я]{3,5}\s[А-Я]{3,5}|'
                                        r'[А-Я]{3,5}и[А-Я]{1,4}|'
                                        r'[А-Я]{3,5})'
                                        r'(?![\wа-яА-Я])')

    def __init__(self):
        self.__segmenter = Segmenter()
        self.__ner_tagger = NewsNERTagger(NewsEmbedding())

    def __cut_academies_by_levels(self, len_levels, academies):
        if len_levels >= len(academies):
            return set(academies)
        return set(academies[:len_levels]
                   + [academy for academy in academies[len_levels:]
                      if any(word in academy.lower() for word in self.__ACADEMIES)])

    def __filter_abbreviations(self, abbreviations):
        return list(filter(lambda x: all(seq not in x for seq in self.__WRONG_ABBREVIATIONS), abbreviations))

    def __normalization(self, academies):
        lst = []
        for name in academies:
            if '"' in name:
                name = remove_invalid_quotes(name)
            if '(' in name or ')' in name:
                name = remove_invalid_brackets(name)

            first_word = name.split()[0]
            cut_name = name
            while first_word[-2:] not in ('ий', 'ый') and first_word.lower() not in self.__ACADEMIES:
                cut_name = ' '.join(cut_name.split()[1:])
                try:
                    first_word = cut_name.split()[0]
                except IndexError:
                    cut_name = name
                    break
            if cut_name.split()[-1].lower() in ('факультет', 'специальность'):
                cut_name = ' '.join(cut_name.split()[:-1])
            if cut_name.lower() not in self.__ACADEMIES:
                lst.append(re.sub(r'\s+', ' ', cut_name))
        return lst

    def __extract_academies(self, text):
        doc = Doc(text.replace('\n', ' '))
        doc.segment(self.__segmenter)
        doc.tag_ner(self.__ner_tagger)
        organizations = [span.text for span in doc.spans if span.type == 'ORG']
        academies = [org for org in organizations if any(academy in org.lower() for academy in self.__ACADEMIES)]
        return self.__normalization(academies) \
            + self.__filter_abbreviations(self.__PATTERN_ABBREVIATION.findall(text))

    def __get_academies(self, full_text, part_text=''):
        if not part_text:
            return self.__normalization(self.__extract_academies(full_text))

        academies = self.__extract_academies(part_text)
        if not academies:
            academies = self.__extract_academies(full_text)
        return self.__normalization(academies)

    def __get_last_year(self, text, count):
        try:
            return max(map(int, self.__PATTERN_YEAR.findall(text)[:count]))
        except ValueError:
            return 0

    def __get_levels(self, text):
        lst = []
        for line in text.split('\n'):
            if any(level in line.lower() for level in self.__LEVELS):
                lst.extend(self.__PATTERN_LEVEL.findall(line.lower()))
        if 'два и более высших' in lst:
            lst.append('высшее')
        return set(lst)

    def __get_idx_of_section(self, indexes, text):
        for i in indexes:
            if len(self.__get_levels(text[i:])):
                return i
        return 0

    def get_info(self, text):
        levels, academies, year, = [], [], 0
        if self.__PATTERN_SECTION.search(text):
            indexes = [match.end() + 1 for match in self.__PATTERN_SECTION.finditer(text)]
            i = indexes[-1]
            if not len(self.__get_levels(text[i:])):
                i = self.__get_idx_of_section(indexes, text)
            levels = self.__get_levels(text[i:])
            year = self.__get_last_year(text[i:], len(levels))
            academies = self.__get_academies(text, text[i:])
        else:
            levels = self.__get_levels(text)
            if len(levels):
                year = self.__get_last_year(text, len(levels))
                academies = self.__get_academies(text)
        return {
            'levels': list(levels),
            'year': year,
            'academies': list(self.__cut_academies_by_levels(len(levels), academies))
        }
