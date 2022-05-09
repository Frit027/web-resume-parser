import spacy
from spacy.matcher import Matcher


class NameExtractor:
    __LIMIT = 300
    __PATTERN = [
        {'ENT_TYPE': 'PER'}
    ]

    def __init__(self):
        self.__nlp = spacy.load('ru_core_news_lg')
        self.__matcher = Matcher(self.__nlp.vocab)

    @staticmethod
    def __is_correct_lemm(tokens):
        return any([token.text.title() == token.lemma_.title() for token in tokens])

    def __get_tokens(self, text):
        self.__matcher.add('full_name', [self.__PATTERN])
        doc = self.__nlp(text)
        matches = self.__matcher(doc)
        return [doc[start:end] for _, start, end in matches]

    def get_info(self, text):
        tokens = self.__get_tokens(text[:self.__LIMIT].replace('\n', ' ').lower())
        full_name = ' '.join(map(lambda x: x.text.title(), tokens))

        if self.__is_correct_lemm(tokens) and len(tokens) in (2, 3):
            return full_name.strip()
        return None
