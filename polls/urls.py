# polls/urls.py

from django.urls import path
from . import views


app_name = 'polls'

urlpatterns = [
    path("list", views.index, name="index"),
    path('write/',views.write, name="write"),
    path('edit',views.edit, name="edit"),
    path('delete',views.delete,name="delete"),
    path('view',views.posting, name="posting"),
    path('download/<str:filename>/',views.download, name="download"),
    path('comment',views.comment,name="comment"),
    path('comment_delete',views.comment_delete,name="comment_delete")
] 