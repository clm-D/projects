from django.db import models

# Create your models here.


class Surnames(models.Model):
    """
    姓氏：
    """
    id = models.IntegerField(primary_key=True, verbose_name='id')
    surname = models.CharField(max_length=32, verbose_name='姓氏')
    nums = models.CharField(max_length=32, verbose_name='数量')

    class Meta:
        db_table = 'surnames'


class Names(models.Model):
    """
    姓名：
    """
    id = models.IntegerField(primary_key=True, verbose_name='id')
    name = models.CharField(max_length=32, verbose_name='姓名')
    surname = models.CharField(max_length=32, verbose_name='姓氏')
    nums = models.CharField(max_length=32, verbose_name='数量')
    boy_progress = models.CharField(max_length=32, verbose_name='男生比例')
    girl_progress = models.CharField(max_length=32, verbose_name='女生比例')
    total_solution = models.CharField(max_length=1024, verbose_name='总解')
    wuxing = models.CharField(max_length=32, verbose_name='五行')

    class Meta:
        db_table = 'names'