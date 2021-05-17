from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.models import User, auth
from django.db.models import Exists
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Detail, Cast
import random
from .utils import send_otp


def login(request):
    if request.method == "GET":
        return render(request, "Login.html")
    else:
        email = request.POST['email']
        email = email.lower()
        '''user = auth.authenticate(username=username)
        if user is None:
            messages.info(request, "Invalid User")
            return redirect("login")
        else:
            user=auth.authenticate(username=username,password=request.POST['password'])
            if user is None:
                messages.info(request, "Invalid Password")
                return redirect("login")
            else:
                auth.login(request, user)
                return redirect("home")'''
        if User.objects.filter(username=email).exists():
            var = User.objects.get(username=email)
            if var.is_active:
                detail=var.name.all().first()
                detail = Detail.objects.get(otp = detail.otp)
                detail.otp = str(random.randint(1000,9999))
                detail.save()
                user = auth.authenticate(username=email, password=request.POST['password'])
                if user is None:
                    messages.info(request, "Incorrect Password")
                    return redirect("login")
                else:
                    send_otp(detail.phone_no,detail.otp)
                    request.session['phone_no'] = detail.phone_no
                    return redirect("otp")
                    # auth.login(request, user)
                    # return redirect("home")
            else:
                messages.info(request, "User Inactive")
                return redirect("login")
        else:
            messages.info(request, "Firstly Create User Here")
            return redirect("create")


@login_required
def home(request):
    return render(request, "Home.html")


def exist(request):
    return render(request, "Exist.html")


def create(request):
    if request.method == "GET":
        return render(request, "Create.html")
    else:
        email = request.POST['email']
        email = email.lower()
        if User.objects.filter(username=email).exists():
            print("hello --------------------------->")
            messages.info(request, "User Already Exists")
            # return render(request,"Create.html",{'message':'User Already exist'})
            return redirect("create")
        else:
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            if password == confirm_password:
                if len(request.POST['phone_no']) == 10:
                    if Detail.objects.filter(phone_no=request.POST['phone_no']).exists():
                        messages.info(request, "Phone No Already Exists")
                        return redirect("create")
                    else:
                        var = User.objects.create_user(username=email, password=request.POST['password'],
                                                       email=email)
                        var.save()
                        otp = str(random.randint(1000, 9999))
                        phone_no = request.POST['phone_no']
                        var2 = Detail(username=var, phone_no=request.POST['phone_no'], otp=otp)
                        var2.save()
                        send_otp(phone_no, otp)
                        request.session['phone_no'] = phone_no
                        return redirect("otp")
                else:
                    messages.info(request, "Invalid Phone_no length")
            else:
                messages.info(request, "Confirm Password Not Matches")
                return redirect("create")


def otp(request):
    phone_no = request.session['phone_no']
    context = {'mobile':phone_no}
    user = User.objects.all()
    # return HttpResponse(phone_no)
    if request.method == "GET":
        return render(request, "otp.html",context)
    else:
        otp = request.POST['otp']
        detail = Detail.objects.get(phone_no=phone_no)
         # print(detail.user.username)
        for i in user:
            if i.username == str(detail.username):
                print("Hello")
                user = User.objects.get(email=i.username)
                break
        # user = User.objects.get(username = user)
        if otp == detail.otp:
            auth.login(request, user)
            return redirect("home")
        else:
            # context = {'message':'Invalid otp','class':'danger','mobile':phone_no}
            messages.info(request,"Invalid otp")
            return render(request,"otp.html",context)

@login_required
def logout(request):
    if request.method == "GET":
        auth.logout(request)
        return redirect("login")


def forgotPassword(request):
    if request.method == "GET":
        return render(request, "Forgot.html")
    else:
        # email = request.POST['email']
        # email = email.lower()
        # if User.objects.filter(username=email).exists():
        #     user = User.objects.get(username=email)
        #     print(user)
        #     user.set_password(request.POST['password'])
        #     user.save()
        #     return redirect("login")
        phone = request.POST['phone_no']
        if Detail.objects.filter(phone_no=phone).exists():
            otp = str(random.randint(1000,9999))
            detail = Detail.objects.get(phone_no = phone)
            detail.otp = otp
            detail.save()
            send_otp(phone,otp)
            request.session['phone'] = phone
            return redirect("Password_otp")
        else:
            messages.info(request, "User Not Exists")
            return redirect("forgotPassword")


def pass_otp(request):
    phone = request.session['phone']
    context = {'mobile':phone}
    if request.method == "GET":
        return render(request,"pass_otp.html",context)
    else:
        detail = Detail.objects.get(phone_no=phone)
        otp = request.POST['otp']
        if otp == detail.otp:
            request.session['phone'] = phone
            return redirect("new_Pass")
        else:
            messages.info(request, "Invalid otp")
            return render(request, "pass_otp.html",context)

def new_password(request):
    phone = request.session['phone']
    user = User.objects.all()
    if request.method == "GET":
        return render(request,"new_pass.html")
    else:
        detail = Detail.objects.get(phone_no=phone)
        # user_id = detail.user.id
        # user = User.objects.get(id=user_id)
        for i in user:
            if i.username == str(detail.username):
                print("Hello")
                user = User.objects.get(email=i.username)
                break
        user.set_password(request.POST['password'])
        user.save()
        return redirect("login")

def enter(request):
    if request.method == "GET":
        return render(request, "Enter.html")
    else:
        if User.objects.filter(username=request.POST['email']).exists():
            var = User.objects.get(username=request.POST['email'])
            return render(request, "Permit.html", {'data': var})
        else:
            messages.info(request, "User Not Exists")
            return redirect("enter")


def permit(request, mid):
    if request.method == "GET":
        var = User.objects.get(id=mid)
        print(var.id)
        if var.is_active:
            var.is_active = False
        else:
            var.is_active = True
    var.save()
    return redirect("login")


def message(request, nid):
    var = Cast.objects.filter(username_id=nid)
    return render(request, "message.html", {'data': var})


