from django.db import models


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
