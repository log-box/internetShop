from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from adminapp.forms import ProductEditForm
from mainapp.models import ProductCategory, Product





class OrdersListView(ListView):
    pass