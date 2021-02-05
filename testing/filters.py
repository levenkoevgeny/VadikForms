import django_filters
from testing.models import Subject, Subdivision, Testing
from django import forms


class SubjectFilter(django_filters.FilterSet):

    subject_name = django_filters.CharFilter(lookup_expr='icontains')
    subdivision = django_filters.ModelMultipleChoiceFilter(queryset=Subdivision.objects.all())

    class Meta:
        model = Subject
        fields = ['subject_name', 'subdivision']



# import django_filters
# from anr.models import ANR
# from authors.models import Author, Subdivision
# from django import forms
#
#
# class ANR_Filter(django_filters.FilterSet):
#
#     HALFYEAR_CHOICES = (
#         (1, 'Первое'),
#         (2, 'Второе'),
#     )
#
#     PARTICIPATION_CHOICES = (
#         (1, 'Да'),
#         (0, 'Нет'),
#     )
#
#     authors = django_filters.ModelMultipleChoiceFilter(queryset=Author.objects.all())
#     subdivisions = django_filters.ModelMultipleChoiceFilter(queryset=Subdivision.objects.all())
#     is_student_participation = django_filters.ChoiceFilter(choices=PARTICIPATION_CHOICES, widget=forms.Select)
#     halfyear = django_filters.ChoiceFilter(choices=HALFYEAR_CHOICES, widget=forms.Select)
#     year_gte = django_filters.NumberFilter(field_name='year', lookup_expr='gte')
#     year_lte = django_filters.NumberFilter(field_name='year', lookup_expr='lte')
#
#     class Meta:
#         model = ANR
#         fields = ['developmentkind', 'introductionkind', 'introductionorganization', 'approvedate', 'halfyear', 'subdivisions', 'year', 'is_student_participation', 'authors']