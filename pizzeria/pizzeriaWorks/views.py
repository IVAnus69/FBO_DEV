from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Pizza, Specifications, Profile
from .forms import UserForm, UserLoginForm


def index(request):
    return render(request, 'index.html')


def update_user_data(user):
    Profile.objects.update_or_create(user=user)#, profilePic=user.profilePic)


def registration(request):
    if request.method == "POST":# and request.FILES:
        form = UserForm(request.POST)
        if form.is_valid():
            #file = request.FILES['profilePic']
            user = form.save()

            user.refresh_from_db()
            #user.profilePic = file
            user.save()

            update_user_data(user)

            profileCheck = Profile.objects.get(user=user)
            login(request, user)
            return HttpResponse("ГУДЕС")
        else:
            return HttpResponse("не туда")
    else:
        form = UserForm()
        return render(request, 'registr.html', {'form': form})


def auth(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponse("Успешно вошел")
    else:
        form = UserLoginForm()
        return render(request, 'auth.html', {'form': form})


def profile(request):
    prof = Profile.objects.get(user=request.user)
    if not prof.profilePic:
        profPic = '/media/images/avatar.jpg'
        bol = False
    else:
        profPic = prof.profilePic
        bol = True
    return render(request, 'profile.html', {'profPic': profPic, 'bol': bol})


def close_log(request):
    logout(request)
    return HttpResponse("Вышел из аккаунта")


def product_view(request):
    products = Pizza.objects.all()
    print(products)
    return render(request, 'product.html', {'products': products})


def product_detail_view(request, pk):
    product = get_object_or_404(Pizza, pk=pk)
    product_spec = Specifications.objects.all().filter(pizza_id=product.id)
    return render(request, 'product_detail.html', {'product': product,
                                                   'product_spec': product_spec})