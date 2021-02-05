import os

from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, FileResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView

from .models import Testing, Subject, Question, Answer
from .forms import TestingForm, SubjectForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from testing.filters import SubjectFilter


@login_required
def test_list(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    if request.user.is_superuser:
        test_l1 = subject.testing_set.all()
        return render(request, 'testing/test_for_subject/testing_list.html', {
            'test_list': test_l1,
            'subject': subject,
        })
    else:
        if subject.subdivision.user == request.user:
            test_l2 = subject.testing_set.all()
            return render(request, 'testing/test_for_subject/testing_list.html', {
                'test_list': test_l2,
                'subject': subject,
            })
        else:
            return HttpResponse("У вас нет прав на просмотр этой страницы!")


@login_required
def test_add(request, subject_id):
    if request.method == 'POST':
        form = TestingForm(request.POST)
        if form.is_valid():
            testing_new = form.save(commit=False)
            testing_new.who_created = request.user
            testing_new.subject = get_object_or_404(Subject, pk=subject_id)
            testing_new.save()
            return JsonResponse({'': ''}, safe=False)
        else:
            error_message = "Заполните форму!"
            return JsonResponse({'error': error_message}, safe=False)
    else:
        form = TestingForm
        return render(request, 'testing/test_for_subject/testing_input_form.html', {
            'form': form,
            'sub_id': subject_id
        })


@login_required
def test_update(request, subject_id, test_id):
    if request.method == "POST":
        test_new = get_object_or_404(Testing, pk=test_id)
        test_new.question_set.all().delete()

        test_new.test_name = request.POST['test_name']
        test_new.description = request.POST['test_description']

        test_new.save()

        question_count = int(request.POST['question_count'])

        for i in range(question_count):
            question_input_text = request.POST['question_input_text_' + str(i)]
            question_has_multiple_choices_select = int(request.POST['question_answer_type_select_' + str(i)])
            if question_has_multiple_choices_select == 2:
                question_has_multiple_choices = True
            elif question_has_multiple_choices_select == 1:
                question_has_multiple_choices = False
                radio_input_value = request.POST['question_' + str(i) + '_answer_is_true_input']

            question_new = Question(
                question=question_input_text,
                has_multiple_choice=question_has_multiple_choices,
                test=test_new
            )
            question_new.save()

            answer_count = int(request.POST['question_' + str(i) + '_answer_count'])

            for j in range(answer_count):
                answer_text = request.POST['question_' + str(i) + '_answer_' + str(j)]
                if question_has_multiple_choices:
                    if 'question_' + str(i) + '_answer_is_true_input_' + str(j) in request.POST:
                        is_true_answer = True
                    else:
                        is_true_answer = False
                else:
                    if answer_text == radio_input_value:
                        is_true_answer = True
                        # answer_weight = 100
                    else:
                        is_true_answer = False
                        # answer_weight = 0
                answer_new = Answer(
                    answer=answer_text,
                    question=question_new,
                    is_true=is_true_answer
                )
                answer_new.save()

            # Расчет весов ответов
            question_for_weight_calculation = get_object_or_404(Question, pk=question_new.id)
            if question_for_weight_calculation.has_multiple_choice:
                true_answer_count = Answer.objects.filter(question=question_for_weight_calculation,
                                                          is_true=True).count()

                if true_answer_count != 0:
                    answer_weight = round((100 / true_answer_count), 3)
                else:
                    answer_weight = 0
                for answer in question_for_weight_calculation.answer_set.all():
                    if answer.is_true:
                        answer.weight = answer_weight
                    else:
                        answer.weight = answer_weight * -1
                    answer.save()
            else:
                for answer in question_for_weight_calculation.answer_set.all():
                    if answer.is_true:
                        answer.weight = 100
                    else:
                        answer.weight = 0
                    answer.save()
        return HttpResponseRedirect(reverse('testing:test_list', kwargs={'subject_id': subject_id}))
    else:
        subject = get_object_or_404(Subject, pk=subject_id)
        test_obj = get_object_or_404(Testing, pk=test_id)
        return render(request, 'testing/test_for_subject/testing_update_form.html', {
            'test_obj': test_obj,
            'subject': subject,
        })


class TestDelete(LoginRequiredMixin, DeleteView):
    template_name = 'testing/test_for_subject/testing_confirm_delete.html'
    model = Testing

    def get_success_url(self):
        test = get_object_or_404(Testing, pk=self.kwargs['pk'])
        subject_id = test.subject.id
        return reverse_lazy('testing:test_list', kwargs={'subject_id': subject_id})


@login_required
def subject_list(request):
    if request.user.is_superuser:
        subject_l = Subject.objects.all()
    else:
        subject_l = Subject.objects.filter(subdivision__user=request.user)
    f = SubjectFilter(request.GET, queryset=subject_l)
    paginator = Paginator(f.qs, 50)
    page = request.GET.get('page')
    subjects = paginator.get_page(page)
    return render(request, 'testing/subject/subject_list.html', {'subject_list': subjects,
                                                                 'filter': f,
                                                                 })


@login_required
def subject_add(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject_new = form.save(commit=False)
            subject_new.subdivision = request.user.subdivision
            subject_new.save()
            return JsonResponse({'': ''}, safe=False)
        else:
            error_message = "Заполните форму!"
            return JsonResponse({'error': error_message}, safe=False)
    else:
        form = SubjectForm
        return render(request, 'testing/subject/subject_input_form.html', {'form': form})


@login_required
def subject_update(request, subject_id):
    if request.method == "GET":
        obj = get_object_or_404(Subject, pk=subject_id)
        form = SubjectForm(instance=obj)
        return render(request, 'testing/subject/subject_update_form.html', {
            'form': form,
            'obj': obj,
        })
    if request.method == "POST":
        obj = get_object_or_404(Subject, pk=subject_id)
        form = SubjectForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'': ''}, safe=False)
        else:
            error_message = "Заполните форму!"
            return JsonResponse({'error': error_message}, safe=False)
    else:
        pass


class SubjectDelete(LoginRequiredMixin, DeleteView):
    template_name = 'testing/subject/subject_confirm_delete.html'
    model = Subject
    success_url = reverse_lazy('testing:subject_list')


def all_tests(request):
    pass


def subdivisions(request):
    pass


def test_download(request, subject_id, test_id):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, "downloads", "file.txt")

    download_test = get_object_or_404(Testing, pk=test_id)

    try:
        somefile = open(file_path, "w")
        try:
            for question in download_test.question_set.all():
                somefile.write('// Start of question: ВопрМножВыбор' + '\n')
                somefile.write(question.question + ' {' + '\n')
                if question.has_multiple_choice:
                    for answer in question.answer_set.all():
                        if answer.is_true:
                            somefile.write('~%' + str(answer.weight) + '%' + answer.answer + '\n')
                        else:
                            somefile.write('~%' + str(answer.weight) + '%' + answer.answer + '\n')
                else:
                    for answer in question.answer_set.all():
                        if answer.is_true:
                            somefile.write('=' + answer.answer + '\n')
                        else:
                            somefile.write('~' + answer.answer + '\n')
                somefile.write('}')
                somefile.write('\n' + '\n')
        except Exception as e:
            print(e)
        finally:
            somefile.close()
    except Exception as ex:
        print(ex)

    return FileResponse(open(file_path, 'rb'))