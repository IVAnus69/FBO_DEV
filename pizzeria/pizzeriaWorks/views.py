from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.views import View
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Pizza, Specifications, Profile, PizzaType, Basket, Order, Order_Item
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


def about(request):
    user_count = User.objects.all().count()
    return user_count

def setCookies(response, request, user):
    profileCheck = Profile.objects.get(user=user)
    response.set_cookie("username", profileCheck.user.username)
    profilePic = get_profile_photo(request)
    response.set_cookie("profilePic", profilePic)
    return response

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
            response = HttpResponseRedirect("/")
            response.set_cookie("username", request.user.username)
            return response
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
                response = HttpResponse("ГУДООО")
                response = setCookies(response, request, prof.user)
                return response
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
        username = request.COOKIES["username"]
        user_counter = about(request)
        # print(profPic)
        return render(request, 'profile.html', {'profPic': profPic,
                                                'username': username,
                                                'bol': bol,
                                                'form': form,
                                                'user_counter': user_counter})




def close_log(request):
    logout(request)
    if request.COOKIES.get("username") and request.COOKIES.get("profilePic"):
        response = HttpResponseRedirect('/')
        response.delete_cookie("username")
        response.delete_cookie("profilePic")
        return response


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
                response = HttpResponseRedirect('/')
                response = setCookies(response, request, user)
                return response
            else:
                return HttpResponse("не туда")
        elif "log" in request.POST:
            formLog = UserLoginForm(request.POST)
            if formLog.is_valid():
                username = formLog.cleaned_data.get("username")
                password = formLog.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                login(request, user)
                response = HttpResponseRedirect('/')
                response = setCookies(response, request, user)
                return response
    else:
        formReg = UserForm();
        formLog = UserLoginForm();

    products = Pizza.objects.all()
    types = PizzaType.objects.all()
    profPic, bol = get_profile_photo(request)
    cart = Basket.objects.all().filter(user_id=request.user.id)
    return render(request, 'product.html', {'products': products,
                                            'types': types,
                                            'profPic' : profPic,
                                            'bol': bol,
                                            'formReg': formReg,
                                            'formLog': formLog,
                                            'cart': cart,
                                            'total_sum': sum(basket.sum() for basket in cart)})


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

def basket_add(request, product_id):
    product = Pizza.objects.get(id=product_id)
    prof = Profile.objects.get(user=request.user)
    baskets = Basket.objects.filter(user_id=prof, pizza_id=product)
    if not baskets.exists():
        Basket.objects.create(user_id=prof, pizza_id=product, count=1)
    else:
        basket = baskets.first()
        basket.count += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def basket_remove(request, product_id):
    product = Pizza.objects.get(id=product_id)
    prof = Profile.objects.get(user=request.user)
    baskets = Basket.objects.filter(user_id=prof, pizza_id=product)
    print(baskets.first().count)
    if baskets.first().count != 1:
        basket = baskets.first()
        basket.count -= 1
        basket.save()
    else:
        baskets.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def modalproduct(request, product_id):
    modal_product = get_object_or_404(Pizza, id=product_id)
    print(modal_product)
    return render(request, 'modal-product.html', {'modal_product': modal_product})

def make_order(request):
    prof = Profile.objects.get(user=request.user)
    basket = Basket.objects.filter(user_id=prof)
    order = Order.objects.create(user_id=prof)
    for b in  basket:
        print(b.count)
        print(b.pizza_id)
        if b.count != 0:
            order_item = Order_Item.objects.create(pizza_id=b.pizza_id, order_id=order, count=b.count)
            order_item.save()

    order.save()
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def ajax_resp(request):
    json = {'text': 'some information'}
    return JsonResponse(json)

def view_order(request):
    prof = Profile.objects.get(user=request.user)
    orders = Order.objects.filter(user_id=prof)
    data = []
    for order in orders:
        order_items = Order_Item.objects.filter(order_id=order)
        data.append([order, order_items])

    data = data[::-1]
    profPic, bol = get_profile_photo(request)
    return render(request, 'orders.html', {'data': data,
                                           'profPic': profPic,
                                           'bol': bol})
