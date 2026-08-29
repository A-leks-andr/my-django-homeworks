# coding=utf-8

from django.db import models


class Book(models.Model):
    name = models.CharField('Название', max_length=64)
    author = models.CharField('Автор', max_length=64)
    pub_date = models.DateField(verbose_name='Дата публикации')

    def __str__(self):
        return f'{self.name} {self.author}'
