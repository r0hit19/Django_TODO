from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login as loginuser,logout
from .forms import  TodoForm
# Create your views here.
from .models import Todo
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method=='GET':
        form=AuthenticationForm()
        context={
            'form':form
        }
        return render(request,'login.html',context=context)
    else:
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                loginuser(request,user)
                return redirect('home')

        else:
            context = {
                'form': form
            }
            return render(request, 'login.html', context=context)



def signup(request):
    if request.method=='GET':
        form=UserCreationForm()
        context={
            'form':form
        }
        return render(request,'signup.html',context=context)
    else:
        form=UserCreationForm(request.POST)
        context = {
            'form': form
        }
        if form.is_valid():
            user=form.save()
            if user is not None:
                return redirect('login')

        else:
            return render(request,'signup.html',context=context)


@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user=request.user
        form=TodoForm()
        todo=Todo.objects.filter(user=user).order_by('priority')
        return render(request,'homepage.html',context={'form':form,'todo':todo,'user':user})


@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user=request.user
        form=TodoForm(request.POST)
        if form.is_valid():
            todo=form.save(commit=False)
            todo.user=user
            todo.save()

            return redirect('home')
        else:
            return render(request,'homepage.html',context={'form':form})

def signout(request):
    logout(request)
    return redirect('login')

def delete_todo(request,id):
    Todo.objects.get(pk=id).delete()
    return redirect('home')


def change_todo(request,id,status):
    todo=Todo.objects.get(pk=id)
    todo.status=status
    todo.save()
    return redirect('home')