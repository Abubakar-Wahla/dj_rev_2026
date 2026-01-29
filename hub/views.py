from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from .models import Project,Tag
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q

class ProjectListView(ListView):
    model=Project
    template_name="hub/projects_list.html"
    context_object_name="projects"
    paginate_by = 2
    ordering=["-created"]

    def get_queryset(self):
        qs=super().get_queryset()

        search=self.request.GET.get("search","").strip()
        tags=self.request.GET.get("tags","").strip()

        if search:
            qs=qs.filter(Q(title__icontains=search)|
                         Q(description__icontains=search)|
                         Q(owner__username__icontains=search)|
                         Q(tags__name__icontains=search))
            
        if tags:
            qs=qs.filter(tags__name__iexact=tags)

        return qs.distinct()

class OwnerRequiredMixin(UserPassesTestMixin):
    """Reusable authorization mixin: only owner can proceed."""

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Not allowed")
        return redirect("hub-projects")

class ProjectCreateView(LoginRequiredMixin,CreateView):
    model=Project
    fields=["title","description","tags"]
    template_name="hub/project_form.html"
    success_url=reverse_lazy("hub-projects")

    def form_valid(self, form):
        form.instance.owner=self.request.user
        return super().form_valid(form)
    

class ProjectUpdateView(LoginRequiredMixin,OwnerRequiredMixin,UpdateView):
    model=Project
    fields=["title","description","tags"]
    template_name="hub/Project_form.html"
    success_url=reverse_lazy("hub-projects")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Project updated successfully")
        return response
    
class ProjectDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Project
    template_name = "hub/project_confirm_delete.html"
    success_url = reverse_lazy("hub-projects")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Project deleted successfully")
        return super().delete(request, *args, **kwargs)
    


