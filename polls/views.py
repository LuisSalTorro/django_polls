from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect 
from django.template import loader
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone

from .models import Question, Choice  # My code stuff

## DetailView expects the captured primary key value from the URL to be called 'pk' (which is why in urls it's <int:pk>)
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # return the last five published questions that exlude future ones
        # below returns everything that is timezone.now and earlier. Ignores future posts
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
        # return Question.objects.order_by('-pub_date')[:5]   # does not ignore future posts

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        # excludes any questions that aren't published yet
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])  # returns the ID of selected choice as string. Is (sent like?) a dictionary-like object
    except (KeyError, Choice.DoesNotExist):  # if a choice wasn't provided, returns a KeyError. Redisplays the question from with an error message if choice isn't given
        # redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't choose an option!",
            })
    else:
        selected_choice.votes = F('votes') + 1  # can be selected_choice.votes += 1 # F('') ensures there is no race condition on db.
        selected_choice.save()  # updates to database?
        # Always return an HttpResponseRedirect after successfully dealing with POST data. NOT DJANGO SPECIFIC. DO Redirect ALWAYS after dealing with POST! It's good practice
        # This prevents data from being posted twice is a user hits the Back button
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))  # reverse call helps avoid havint to hardcode a URL



##########BELOW Old way of doing things. Less versitle I guess, and requires more python code ####################
# # Create your views here.
# def index(request):
#     #display the 5 more recent questions in the system according to publication date
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     #output = ', '.join([q.question_text for q in latest_question_list]) # <-hardcoded solution
#     context = {
#         'latest_question_list': latest_question_list
#     }
#     return render(request, 'polls/index.html', context)

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)  # if obj exists, gets obj. else returns 404 page
#     return render(request, 'polls/detail.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
