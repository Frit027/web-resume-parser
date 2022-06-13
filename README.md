<h1 align="center">Web Resume Parser</h1>

## Description
### General description
The project combines the technologies of a classic client-server application and NLP tools.
### Web site
The main task of the website is to accept files (.pdf or .docx) from the user of resumes of
applicants in the IT field, then extract the main information from the resume using a parser
and bring it to a structured form.
After that, based on the received data, filters are formed, with the help of which the user
can select resumes according to certain criteria.
### Parser
The parser extracts information such as name, email, phone number, degree of education,
completed educational institutions, work experience, as well as a list of available
computer skills (programming languages, frameworks, etc.) and puts it in a JSON file.

## Getting Started
1. Clone this repository to your directory.
2. If necessary, change the database connection settings in the file [my.cnf](my.cnf).
3. Run the following commands:
   1. `python manage.py makemigrations`
   2. `python manage.py migrate`
4. Insert the data from the files in [resume/static/txt](resume/static/txt) into the appropriate tables and run the command:
   1. `python manage.py runserver`

## Usage
Web service access link: [http://yurov.pythonanywhere.com/](http://yurov.pythonanywhere.com/)

## Technologies
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
- [Regular expressions](https://docs.python.org/3/library/re.html) `[3.8]` - search for years, abbreviations, phone numbers, etc.
- [spaCy](https://spacy.io/) `[3.3]` - email and name recognition
- [Natasha](https://github.com/natasha/natasha) `[1.4.0]` - recognition of educational institutions

### Parser schema
![Parser schema](assets/scheme-en.png)

## Demonstration
![Demonstration](assets/demonstration.gif)