from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core.files.storage import FileSystemStorage


def index(request):
    return render(request, 'index.html')