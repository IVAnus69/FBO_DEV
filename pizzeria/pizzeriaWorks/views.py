from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.views import View
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Pizza, Specifications, Profile, PizzaType
from .forms import UserForm, UserLoginForm, ChangeUserProfile
from django.contrib.auth.models import User


class Ajax2View(View):
    def post(self, request):
        message = 'Это сообщение получено от сервера с помощью AJAX'
        data = {
             'message': message
        }
        print(123)
        return JsonResponse(data)
    def get(self, request):
        message = '123'
        data = {
             'message': message
        }
        print(123)
        return JsonResponse(data)


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
            return HttpResponseRedirect('/')
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
            return HttpResponseRedirect('/')
    else:
        form = UserLoginForm()
        return render(request, 'auth.html', {'form': form})


def profile(request):
    if request.method == 'POST':
        if 'saveButton' in request.POST:# and request.FILES:
            form = ChangeUserProfile(request.POST)
            if form.is_valid():
                prof = Profile.objects.get(user=request.user)
                if request.POST.get("profilePic") != '':
                    file = request.FILES['profilePic']
                    prof.profilePic = file
                prof.user.username = request.POST.get("username")

                if User.objects.filter(email=request.POST.get("email")).count() == 0:
                    prof.user.email = request.POST.get("email")

                if request.POST.get("password") != '':
                    prof.user.set_password(request.POST.get("password"))
                prof.user.save()
                prof.save()
                login(request, prof.user)
                return HttpResponse("ГУДООО")
            return HttpResponseRedirect('/')

        elif 'deleteButton' in request.POST:
            return HttpResponse("Удалил типа")
    else:
        prof = Profile.objects.get(user=request.user)
        initial_dict = {
            "username": prof.user.username,
            "email": prof.user.email
        }
        form = ChangeUserProfile(initial=initial_dict)
        if not prof.profilePic:
            profPic = '/media/images/avatar.jpg'
            bol = False
        else:
            profPic = prof.profilePic
            bol = True
        return render(request, 'profile.html', {'profPic': profPic, 'bol': bol, 'form': form})




def close_log(request):
    logout(request)
    return HttpResponseRedirect('/')


def product_view(request):
    if request.method == "POST":
        if "reg" in request.POST:
            formReg = UserForm(request.POST)
            if formReg.is_valid():
                #file = request.FILES['profilePic']
                user = formReg.save()

                user.refresh_from_db()
                #user.profilePic = file
                user.save()

                update_user_data(user)

                profileCheck = Profile.objects.get(user=user)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("не туда")
        elif "log" in request.POST:
            formLog = UserLoginForm(request.POST)
            if formLog.is_valid():
                username = formLog.cleaned_data.get("username")
                password = formLog.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect('/')
    else:
        formReg = UserForm();
        formLog = UserLoginForm();

    products = Pizza.objects.all()
    types = PizzaType.objects.all()
    profPic, bol = get_profile_photo(request)
    return render(request, 'product.html', {'products': products,
                                            'types': types,
                                            'profPic' : profPic,
                                            'bol': bol,
                                            'formReg': formReg,
                                            'formLog': formLog})


def product_detail_view(request, pk):
    product = get_object_or_404(Pizza, pk=pk)
    print(product.isAlive == True)
    product_spec = Specifications.objects.all().filter(pizza_id=product.id)
    profPic, bol = get_profile_photo(request)
    return render(request, 'product_detail.html', {'product': product,
                                                   'product_spec': product_spec,
                                                   'profPic': profPic,
                                                   'bol': bol})


def get_profile_photo(request):
    if request.user.is_authenticated:
        prof = Profile.objects.get(user=request.user)
        if not prof.profilePic:
            profPic = '/media/images/avatar.jpg'
            bol = False
        else:
            profPic = prof.profilePic
            bol = True
    else:
        profPic = '/media/images/avatar.jpg'
        bol = False

    return profPic, bol


def product_delete(request, pk):
    product = get_object_or_404(Pizza, pk=pk)
    product.isAlive = False
    product.save()
    return HttpResponseRedirect('/')