from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="hub-projects"),
    path("create/", views.ProjectCreateView.as_view(), name="hub-project-create"),
    path("<uuid:pk>/edit/", views.ProjectUpdateView.as_view(), name="hub-project-edit"),
    path("<uuid:pk>/delete/", views.ProjectDeleteView.as_view(), name="hub-project-delete"),
]
