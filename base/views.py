from encodings import search_function

from django.shortcuts import render, redirect
from django.template.defaultfilters import title
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from base.models import Task
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, FormMixin
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin


from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth import  login




# Create your views here.
# Class based list view derived from class ListView to display a list of items
class TaskList(LoginRequiredMixin, ListView):

    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)


        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__startswith=search_input)

        context['search_input'] = search_input
        return context
# Class based view to display details of an object , inerit from detailview class
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task' # This is custom object name to retrieve data from database throught html
    # Here we cann define our cutom template name for detail view objec
    template_name = 'base/task.html'
# Create view class inherited from createview to perform CRUD



class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
  # Here you can define your own choice of fields from model test
   # field =['title', 'description','']

    # Here you can add all the present fields to view
   # fields='__all__'
    fields=['title','description','complete']
    success_url = reverse_lazy('tasks')

    def form_invalid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model =  Task
    fields=['title','description','complete']
    success_url = reverse_lazy('tasks')

class DeleteTask (LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


# Login View

class UserLogin(LoginView):

    template_name = 'base/login.html'
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class UserRegister(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserRegister, self).form_valid(form)


    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(UserRegister, self).get(*args,**kwargs)