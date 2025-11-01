<h1>
    <div align="right">
        <a href="README.md"><img src="https://cdn.jsdelivr.net/gh/lipis/flag-icons/flags/4x3/us.svg" width="32" alt="Английский язык" title="Английский язык"/></a>
        <code><a href="#"><img src="https://cdn.jsdelivr.net/gh/lipis/flag-icons/flags/4x3/ru.svg" width="32" alt="Русский язык" title="Русский язык"/></a></code>
    </div>
    Web Resume Parser
</h1>

## Описание
### Общее описание
Проект сочетает в себе технологии классического клиент-серверного приложения и инструменты направления NLP.
### Веб-сайт
Основной задачей веб-сайта является получение от пользователя файлов (.pdf или .docx) резюме соискателей IT-сферы,
последующего извлечения из текста резюме главной информации с помощью парсера и приведение её к структурированному виду.
После этого на основе полученных данных формируются фильтры, с помощью которых пользователь может отбирать
резюме по тем или иным критериям.
### Парсер
Парсер извлекает такую информацию, как имя, email, номер телефона, степень образования, оконченные учебные заведения,
опыт работы, а также список имеющихся компьютерных навыков (языки программирования, фреймворки и т.д.) и помещает её
в JSON-файл.

## Демонстрация
![Демонстрация](assets/demonstration.gif)

## Установка
1. Клонируйте данный репозиторий в вашу директорию.
2. При необходимости измените настройки подключения к базе данных в файле [my.cnf](my.cnf).
3. Выполните следующие команды:
   - `python manage.py makemigrations`
   - `python manage.py migrate`
4. Заполните соответствующие таблицы данными из файлов в [resume/static/txt](resume/static/txt) и выполните команду:
   - `python manage.py runserver`

## Использование
Веб-сервис доступен по ссылке: [http://yurov.pythonanywhere.com/](http://yurov.pythonanywhere.com/)

## Технологии
### Backend
- [Python](https://www.python.org/) `[3.8]`
- [Django](https://www.djangoproject.com/) `[4.0]`
- [MySQL](https://www.mysql.com/) `[8.0]`
### Frontend
- [HTML5](https://dev.w3.org/html5/html-author/)
- [Django template language](https://docs.djangoproject.com/en/4.0/ref/templates/language/) `[4.0]`
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) `[ES9]`
- [jQuery](https://jquery.com/) `[3.6.0]`
- [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [Bootstrap](https://getbootstrap.com/) `[5.1.3]`
### Parser (NLP)
- [Regular expressions](https://docs.python.org/3/library/re.html) `[3.8]` - поиск годов, аббревиатур, номеров телефонов и тд.
- [spaCy](https://spacy.io/) `[3.3]` - распознавание email и имён
- [Natasha](https://github.com/natasha/natasha) `[1.4.0]` - распознавание учебных заведений

### Схема парсера
![Схема парсера](assets/scheme-ru.png)
