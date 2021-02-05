from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from testing.models import Subject, Testing, Answer
from testing.filters import SubjectFilter
from django.core.paginator import Paginator

from .filters import ResultDataFilter
from .models import ResultData
from django.urls import reverse


def subject_list(request):
    f = SubjectFilter(request.GET, queryset=Subject.objects.all())
    paginator = Paginator(f.qs, 50)
    page = request.GET.get('page')
    subjects = paginator.get_page(page)
    return render(request, 'training/subject_list.html', {'subject_list': subjects,
                                                          'filter': f,
                                                          })


def test_list(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    test_l = subject.testing_set.all()
    return render(request, 'training/test_list.html', {
        'test_list': test_l,
        'subject': subject,
    })


def test_passing(request, subject_id, test_id):
    if request.method == 'POST':
        score = 0

        user_answers_list = []

        test = get_object_or_404(Testing, pk=test_id)
        for question in test.question_set.all():
            if question.has_multiple_choice:
                true_answers = Answer.objects.filter(question=question, is_true=True)
                true_answers_weight = true_answers.first().weight
                for i in range(question.answer_set.all().count()):
                    if 'question_' + str(question.id) + '_checkbox_' + str(i) in request.POST:
                        user_answer_checkbox_id = request.POST['question_' + str(question.id) + '_checkbox_' + str(i)]
                        user_answers_list.append(int(user_answer_checkbox_id))
                        user_answer_checkbox = get_object_or_404(Answer, pk=user_answer_checkbox_id)
                        if user_answer_checkbox in true_answers:
                            score = score + true_answers_weight
            else:
                true_answer = Answer.objects.filter(question=question, is_true=True).first()
                user_answer = request.POST['question_' + str(question.id) + '_radio']
                user_answers_list.append(int(user_answer))
                if true_answer.id == int(user_answer):
                    score = score + 100
        total_score = round(score / test.question_set.all().count())
        answers_str = ''
        for user_answer in user_answers_list:
            answers_str = answers_str + str(user_answer) + ','

        result = ResultData(
            learner_fio=request.POST.get('fio', ''),
            score=total_score,
            test=get_object_or_404(Testing, pk=test_id),
            answers=answers_str
        )
        result.save()

        return HttpResponseRedirect(reverse('training:test_result', kwargs={
            'subject_id': subject_id,
            'test_id': test_id,
            'result_id': result.id,
        }))

    else:
        test = get_object_or_404(Testing, pk=test_id)
        return render(request, 'training/test_passing.html', {'test': test})


def test_result(request, subject_id, test_id, result_id):
    result = get_object_or_404(ResultData, pk=result_id)
    total_score = result.score
    test = result.test
    user_answers_list_str = list(result.answers.split(","))
    del user_answers_list_str[-1]

    map_object = map(int, user_answers_list_str)
    user_answers_list_int = list(map_object)

    return render(request, 'training/test_result.html',
                  {'total_score': total_score,
                   'test': test,
                   'user_answers_list': user_answers_list_int,
                   })


@login_required
def test_all_results(request):
    user = request.user
    if user.is_superuser:
        results_l = ResultData.objects.all()
    else:
        results_l = ResultData.objects.filter(test__subject__subdivision__user=user)
    f = ResultDataFilter(request.GET, queryset=results_l)
    paginator = Paginator(f.qs, 50)
    page = request.GET.get('page')
    results = paginator.get_page(page)
    return render(request, 'training/test_all_results.html', {
        'results': results,
        'filter': f,
    })
