from django.urls import path
from . import views

app_name = 'polls'  # Prevents other apps accessing these urls and messing the website up
                    # a way there might issues is if another app has their own views.detial, or view.results. You get the idea.


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]



# Less generic way of writing the views BELOW
# urlpatterns = [
#     #example: /polls/
#     path('', views.index, name='index'),
#     #ex: /polls/5/  ###specifics if option. Can be allowed because index.html is now more flexible
#     path('anythingIwantLOL/<int:question_id>/', views.detail, name='detail'),
#     #ex: /polls/5/results/
#     path('<int:question_id>/results/', views.results, name='results'),
#     #ex: /polls/5/vote/
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]