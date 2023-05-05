from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic.edit import UpdateView

from django.http import HttpResponse

from datetime import datetime

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Task

from .forms import LoginForm, AddTask, RegisterForm, EditForm

# Create your views here.
class Login(View):
    def get(self, request):
        form = LoginForm()
        if self.request.user.is_authenticated:
            return redirect('home')
        return render(request, 'base/login.html', {
            'form': form
        })
    
    def post(self, request):
        form = LoginForm(request.POST)
        
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user=user)
                return redirect('home')
            else:
                is_wrong = True
        else:
            form = LoginForm()
        
        return render(request, 'base/login.html', {
            'form': form,
            'is_wrong': is_wrong
        })
    
class Register(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('home')
        form = RegisterForm()
        return render(request, 'base/register.html', {
            'form': form
        })

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            register = User(username=username, password=make_password(password), first_name=first_name, last_name=last_name)
            register.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

        return render(request, 'base/register.html', {
            'form': form
        })

class Base(View):
    def get(self, request):
        AddTaskForm = AddTask()
        if self.request.user.is_authenticated:
            all_task = Task.objects.all()
            user_task = all_task.filter(user=self.request.user, status=False).order_by('-created')
            done_task = all_task.filter(user=self.request.user, status=True).order_by('-done')

            if request.GET.get('done'):
                id = request.GET.get('done')
                try:
                    set_done = Task.objects.get(id=id, user=self.request.user)
                    set_done.status = True
                    set_done.done = datetime.now()
                    set_done.save()
                except:          
                    pass
            elif request.GET.get('delete'):
                id = request.GET.get('delete')
                try:
                    delete = Task.objects.get(id=id, user=self.request.user)
                    delete.delete()
                except:
                    pass
            elif request.GET.get('undone'):
                try:
                    id = request.GET.get('undone')
                    undone = Task.objects.get(id=id, user=self.request.user)
                    undone.status = False
                    undone.save()
                except:
                    pass
        else:
            user_task = None
            done_task = None
        return render(request, 'base/base.html', {
            'atform': AddTaskForm,
            'task': user_task,
            'done_task': done_task
        })
    
    def post(self, request):
        if self.request.user.is_anonymous:
            return redirect('login')
        AddTaskForm = AddTask(request.POST)

        if AddTaskForm.is_valid():
            task_name = AddTaskForm.cleaned_data['taskname']
            create_task = Task(todo=task_name, user=self.request.user)
            create_task.save()
            AddTaskForm = AddTask()
            return redirect('home')

        else:
            AddTaskForm = AddTask()

        return render(request, 'base/base.html', {
            'atform': AddTaskForm
        })
    

class EditTask(View):
    def get(self, request, id):
        if self.request.user.is_authenticated:
            try:
                task = Task.objects.get(id=id, user=self.request.user, status=False)
            except:
                return HttpResponse('<h1>Access denied</h1>')
        editform = EditForm()
        editform['todo'].initial = task.todo
        return render(request, 'base/edit-task.html', {
            'task': task,
            'form': editform
        })
    
    def post(self, request, id):
        editform = EditForm(request.POST)
        task = Task.objects.get(id=id, user=self.request.user, status=False)
        
        if editform.is_valid():
            edit = editform.cleaned_data['todo']
            task.todo = edit
            task.save()
            return redirect('home')
        else:
            editform = EditForm()

        return render(request, 'base/edit-task.html', {
            'task': task,
            'form': editform
        })
    



