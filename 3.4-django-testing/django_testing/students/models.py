from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Student(models.Model):
    name = models.TextField()

    birth_date = models.DateField(
        null=True,
    )

    def __str__(self) -> str:
        return f"Студент {self.name}, {self.birth_date} года рождения"


class Course(models.Model):
    name = models.TextField()

    students = models.ManyToManyField(
        Student,
        blank=True,
    )

    def __str__(self) -> str:
        return f"Курс {self.name}"

    def clean(self) -> None:
        super().clean()
        if self.pk and self.students.count() > settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError(
                "На курсе не может быть больше "
                f"{settings.MAX_STUDENTS_PER_COURSE} студентов."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
