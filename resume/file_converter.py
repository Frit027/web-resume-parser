from pdfminer.high_level import extract_text
import docx2txt


class FileConverter:
    __STOP_WORDS = ('Резюме обновлено', 'Created with', 'please visit: http', 'Образец резюме')

    @staticmethod
    def __clean_text(text):
        return text.replace(u'\xa0', u' ').replace(u'\x00', u' ')

    def __remove_uninformative_lines(self, text):
        return '\n'.join([line for line in text.splitlines()
                          if line
                          and not any(word in line for word in self.__STOP_WORDS)])

    def __pdf_to_text(self, file):
        return self.__clean_text(self.__remove_uninformative_lines(extract_text(file)))

    def __docx_to_txt(self, file):
        return self.__clean_text(self.__remove_uninformative_lines(docx2txt.process(file)))

    def get_text(self, path):
        extension = path[path.rfind('.') + 1:]
        if extension.lower() == 'pdf':
            return self.__pdf_to_text(path)
        elif extension.lower() == 'doc':
            pass
        elif extension.lower() == 'docx':
            return self.__docx_to_txt(path)
