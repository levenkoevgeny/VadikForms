from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User


class Subdivision(models.Model):
    subdivision_name = models.CharField(max_length=255, verbose_name="Кафедра")
    user = models.OneToOneField(User, on_delete=models.SET_NULL, verbose_name="Пользователь", blank=True, null=True)

    def __str__(self):
        return self.subdivision_name

    class Meta:
        ordering = ('subdivision_name',)
        verbose_name = 'Кафедра'
        verbose_name_plural = 'Кафедры'


class Subject(models.Model):
    subject_name = models.CharField(max_length=255, verbose_name="Предмет")
    subdivision = models.ForeignKey(Subdivision, on_delete=models.CASCADE, verbose_name="Кафедра")

    def __str__(self):
        return self.subject_name

    class Meta:
        ordering = ('subject_name',)
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Testing(models.Model):
    test_name = models.CharField(max_length=255, verbose_name="Название теста")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    date_added = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    date_last_editing = models.DateTimeField(verbose_name="Время последнего редактирования", auto_now=True)
    who_created = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Кто создал тест")

    def __str__(self):
        return self.test_name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    question = models.TextField(verbose_name="Вопрос")
    date_added = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    test = models.ForeignKey(Testing, on_delete=models.CASCADE, verbose_name="Тест")
    has_multiple_choice = models.BooleanField(verbose_name="Имеет несколько ответов")

    def __str__(self):
        return self.question

    class Meta:
        ordering = ('id',)
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    answer = models.TextField(verbose_name="Ответ")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    is_true = models.BooleanField(verbose_name="Является верным")
    weight = models.FloatField(verbose_name="Вес ответа", blank=True, null=True)

    def __str__(self):
        return self.answer + ' к вопросу - ' + self.question.question + ' является верным - ' + str(self.is_true) + ' вес = ' + str(self.weight)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'