from django.forms import ModelForm
from .models import Testing, Subject


class TestingForm(ModelForm):

    class Meta:
        model = Testing
        fields = ['test_name', 'description']


class SubjectForm(ModelForm):

    class Meta:
        model = Subject
        fields = ['subject_name']
