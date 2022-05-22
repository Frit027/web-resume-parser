import json as json_lib
import os
from functools import reduce
from django.db import models
from django.contrib.auth.models import User
from web_resume_parser.settings import SKILLS


class Resume(models.Model):
    filename = models.CharField(max_length=255, default='filename')
    file = models.FileField(upload_to='resume')
    json = models.FileField(upload_to='resume/json', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'resume'

    @property
    def data(self):
        with open(self.json.path, 'r', encoding='utf-8') as f:
            return json_lib.load(f)

    @staticmethod
    def __get_all_resumes(user):
        return {resume: resume.data for resume in user.resume_set.all()}

    @staticmethod
    def __filter_by_age(interval_ages, resumes):
        if interval_ages == 'None':
            return resumes
        if interval_ages == '14_20':
            interval = tuple(range(14, 20))
        elif interval_ages == '20_30':
            interval = tuple(range(20, 30))
        elif interval_ages == '30_50':
            interval = tuple(range(30, 50))
        else:
            interval = tuple(range(50, 100))
        return [resume for resume in resumes if resumes[resume]['age'] in interval]

    @staticmethod
    def __filter_by_experience(exp, resumes):
        if exp == 'None':
            return resumes
        if exp == 'no':
            return [resume for resume in resumes if resumes[resume]['experience'] is None]
        if exp == 'less_1':
            def is_in_interval(age): return age < 1
        elif exp == '1_3':
            def is_in_interval(age): return 1 <= age < 3
        elif exp == '3_5':
            def is_in_interval(age): return 3 <= age < 5
        elif exp == '5_10':
            def is_in_interval(age): return 5 <= age < 10
        else:
            def is_in_interval(age): return age >= 10
        return [resume for resume in resumes
                if resumes[resume]['experience'] is not None and is_in_interval(resumes[resume]['experience'])]

    @staticmethod
    def __filter_by_levels(levels, resumes):
        if not levels:
            return resumes
        return [resume for resume in resumes if set(resumes[resume]['education']['levels']) & set(levels)]

    @staticmethod
    def __list_merge(lst): return reduce(lambda d, el: d.extend(el) or d, lst, [])

    @staticmethod
    def __filter_by_skills(skills, resumes):
        if not Resume.__list_merge(skills.values()):
            return resumes
        res = []
        for resume in resumes:
            if set(Resume.__list_merge(resumes[resume]['skills'].values())) & set(Resume.__list_merge(skills.values())):
                res.append(resume)
        return res

    @staticmethod
    def get_resumes_by_filters(user, interval_ages, exp, levels, skills):
        resumes = Resume.__get_all_resumes(user)
        resumes_by_age = Resume.__filter_by_age(interval_ages, resumes)
        resumes_by_exp = Resume.__filter_by_experience(exp, resumes)
        resumes_by_levels = Resume.__filter_by_levels(levels, resumes)
        resumes_by_skills = Resume.__filter_by_skills(skills, resumes)

        return set(resumes_by_skills) & set(resumes_by_levels) & set(resumes_by_exp) & set(resumes_by_age)

    @staticmethod
    def get_selectors(user):
        data = {}
        for resume in Resume.__get_all_resumes(user).values():
            data['levels'] = resume['education']['levels'] + data.get('levels', [])
            for skill in SKILLS:
                data[skill] = resume['skills'][skill] + data.get(skill, [])
        return {k: sorted(list(set(v))) for k, v in data.items()}

    @staticmethod
    def get_json_response(resumes):
        response = []
        for resume in resumes:
            data = resume.data
            data['filename'] = resume.filename
            response.append(data)
        return response

    @staticmethod
    def get_filenames(user):
        return [resume.filename for resume in user.resume_set.all()]

    @staticmethod
    def remove_files(user):
        for resume in user.resume_set.all():
            os.remove(resume.file.path)
            os.remove(resume.json.path)
            resume.delete()


class Skill(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        abstract = True

    @classmethod
    def get_all(cls):
        return [obj.name for obj in cls.objects.all()]


class Android(Skill):
    class Meta:
        db_table = 'android'


class Backend(Skill):
    class Meta:
        db_table = 'backend'


class DB(Skill):
    class Meta:
        db_table = 'db'


class DevOps(Skill):
    class Meta:
        db_table = 'devops'


class Frontend(Skill):
    class Meta:
        db_table = 'frontend'


class GameDev(Skill):
    class Meta:
        db_table = 'gamedev'


class IOS(Skill):
    class Meta:
        db_table = 'ios'


class MarkupLang(Skill):
    class Meta:
        db_table = 'markup_lang'


class ML(Skill):
    class Meta:
        db_table = 'ml'


class OperatingSystem(Skill):
    class Meta:
        db_table = 'operating_system'


class ProgramLang(Skill):
    class Meta:
        db_table = 'program_lang'


class SkillWithSlash(Skill):
    class Meta:
        db_table = 'skill_with_slash'


class StylesheetLang(Skill):
    class Meta:
        db_table = 'stylesheet_lang'


class SysAdmin(Skill):
    class Meta:
        db_table = 'sys_admin'


class Testing(Skill):
    class Meta:
        db_table = 'testing'


class VersionControl(Skill):
    class Meta:
        db_table = 'version_control'
