import re
import spacy
from spacy.matcher import Matcher


class ContactInfoExtractor:
    __PATTERN_EMAIL = [
        {'LIKE_EMAIL': True}
    ]
    __PATTERN_PHONE = re.compile(r'(?<![\wа-яА-Я])(?:\+7|8|7)[-\s(]*\d{3}[-)\s]*\d{3}[\s-]?\d{2}[\s-]?\d{2}(?![\wа-яА-Я])')

    def __init__(self):
        self.__nlp = spacy.load('ru_core_news_lg')
        self.__matcher = Matcher(self.__nlp.vocab)

    def __extract_email(self, text):
        self.__matcher.add('email', [self.__PATTERN_EMAIL])
        doc = self.__nlp(text)
        matches = self.__matcher(doc)
        emails = [doc[start:end].text for _, start, end in matches]
        return emails[0] if emails else None

    def __extract_phone(self, text):
        match = self.__PATTERN_PHONE.search(text)
        return match.group(0) if match else None

    def get_info(self, text):
        return self.__extract_email(text), self.__extract_phone(text)
