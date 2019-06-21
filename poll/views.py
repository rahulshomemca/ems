from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from poll.models import *
from django.contrib.auth.models import User
from django.views.generic import View
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
from django.db.models import Q
from ems.decorators import *
from poll.forms import PollForm, ChoiceForm
from poll.models import *

class PollView(View):
    decorators = [login_required, admin_hr_required]

    @method_decorator(decorators)
    def get(self, request, id=None):
        if id:
            question = get_object_or_404(Question, id=id)
            poll_form = PollForm(instance=question)
            choices = question.choice_set.all()
            choice_forms = [ChoiceForm(prefix=str(choice.id), instance=choice) for choice in choices]
            template = 'poll/edit_poll.html'
        else:
            poll_form = PollForm(instance=Question())
            choice_forms = [ChoiceForm(prefix=str(x), instance=Choice()) for x in range(3)]
            template = 'poll/new_poll.html'
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, template, context)

    @method_decorator(decorators)
    def post(self, request, id=None):
        context = {}
        if id:
            return self.put(request, id)
        poll_form = PollForm(request.POST, instance=Question())
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            x), instance=Choice()) for x in range(0, 3)]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.questions_id = new_poll.id
                new_choice.save()
            messages.success(request, 'New Poll has been added successfully')
            return HttpResponseRedirect('/polls/all_poll')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'poll/new_poll.html', context)

    @method_decorator(decorators)
    def put(self, request, id=None):
        context = {}
        question = get_object_or_404(Question, id=id)
        poll_form = PollForm(request.POST, instance=question)
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            choice.id), instance=choice) for choice in question.choice_set.all()]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            messages.success(request, 'Poll has been updated successfully')
            return redirect('all_poll')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'poll/edit_poll.html', context)

@login_required(login_url="/login/")
@admin_hr_required
def delete(request, id=None):
    try:
        question = Question.objects.get(id=id)
    except:
        raise Http404
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Poll has been deleted successfully')
        return HttpResponseRedirect(reverse('all_poll'))
    else:
        context = {}
        context['question'] = question
        return render(request, 'poll/delete.html', context)

@login_required(login_url="/login/")
@admin_hr_required
def all_poll(request):
    context = {}
    questions = Question.objects.all()
    context['title'] = 'EMS | List of Questions'
    context['questions'] = questions
    return render(request, 'poll/all_poll.html', context)

@login_required(login_url="/login/")
def index(request):
    context = {}
    questions = Question.objects.all()
    context['title'] = 'EMS | List of Questions'
    context['questions'] = questions
    return render(request, 'poll/index.html', context)

@login_required(login_url="/login/")
def details(request, id):
    context = {}
    try:
        question = Question.objects.get(id=id)
    except:
        raise Http404
    context['title'] = 'Result | '+question.title
    context['question'] = question
    return render(request, 'poll/details.html', context)

@login_required(login_url="/login/")
@emp_only
def polls(request, id):
    if request.method == "GET":
        context = {}
        try:
            question = Question.objects.get(id=id)
        except:
            raise Http404
        context['title'] = 'Vote | '+question.title
        context['question'] = question
        return render(request, 'poll/poll.html', context)
    if request.method == "POST":
        user_id = request.user.id
        data = request.POST
        question = Question.objects.get(id=id)
        ans = Answer.objects.filter(user_id=user_id, question_id=question.id)
        if ans:
            messages.warning(request, 'Your Vote already submitted')
            return redirect('polls_list')
        else:
            ret = Answer.objects.create(user_id=user_id, choice_id=data['choice'], question_id=question.id)
            if ret:
                messages.success(request, 'Your Vote submitted Succesfully')
                return redirect('polls_list')
            else:
                messages.danger(request, 'Vote not Submitted')
                return redirect('polls_list')


