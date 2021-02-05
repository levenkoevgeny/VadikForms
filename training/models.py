from django.db import models
from testing.models import Testing


class ResultData(models.Model):
    learner_fio = models.CharField(max_length=255, verbose_name="Данные обучающегося")
    test_date = models.DateTimeField(verbose_name="Дата прохождения теста", auto_now_add=True)
    score = models.FloatField(verbose_name="Результат теста", blank=True, null=True)
    test = models.ForeignKey(Testing, on_delete=models.CASCADE, verbose_name="Данные по тесту")
    answers = models.CharField(max_length=255, verbose_name="Ответы", blank=True, null=True)

    def __str__(self):
        return self.learner_fio

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Результат тестирования'
        verbose_name_plural = 'Результаты тестирования'




