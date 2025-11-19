from django.http import HttpResponse
from django.shortcuts import render, redirect

from fruitipediaApp.fruits.forms import CategoryForm, FruitAddForm, EditFruitForm , FruitDeleteForm
from fruitipediaApp.fruits.models import Fruit,Category


# Create your views here.

def index_view(request):
    return render(request,'common/index.html')

def dashboard_view(request):
    fruits = Fruit.objects.all()
    context = {'fruits':fruits}

    return render(request,'common/dashboard.html',context)

def create_fruit(request):
    if request.method == "GET":
        form = FruitAddForm()
    elif request.method == "POST":
        form = FruitAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form':form}
    return render(request,'fruits/create-fruit.html', context)

def fruit_details_view(request,pk):
    fruit = Fruit.objects.get(id=pk)
    context = {'fruit':fruit}
    return render(request, 'fruits/details-fruit.html',context)

def edit_fruit_view(request,pk):
    fruit = Fruit.objects.get(id=pk)
    if request.method == "GET":
        form = EditFruitForm(instance=fruit)
    elif request.method == "POST":
        form = EditFruitForm(request.POST, instance=fruit)
        if form.is_valid():
            fruit.save()
            return redirect('dashboard')

    context = {'form':form, 'fruit':fruit}
    return render(request, 'fruits/edit-fruit.html',context)

def delete_fruit_view(request,pk):
    fruit = Fruit.objects.get(id=pk)
    if request.method == "GET":
        form = FruitDeleteForm(instance=fruit)
    else:
        form = FruitDeleteForm(request.POST, instance=fruit)
        fruit.delete()
        return redirect('dashboard')

    context = {'form':form, 'fruit':fruit}
    return render(request, 'fruits/delete-fruit.html',context)

def create_category_view(request):
    if request.method == "GET":
        form = CategoryForm()
    elif request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form':form}

    return render(request, 'categories/create-category.html', context)
