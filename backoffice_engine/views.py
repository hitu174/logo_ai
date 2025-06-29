from django.shortcuts import render,redirect
from backoffice_engine.models import *
from backoffice_engine.forms import UserForm,UserUpdate
from backoffice_engine import *
import sys
from django.contrib import messages
import random
from LogoAi import settings
from django.core.mail import send_mail
from datetime import date,timedelta
from .models import Category , Logo
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from backoffice_engine.utils import text2vision
import re 
from django.utils import timezone
from datetime import timedelta



def index(request):
    f =  Feedback.objects.all()
    return render(request ,'index.html',{'f':f})

def about(request):
    return render(request,'about.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import User, Subscription, Plan  # Adjust based on your project

def login(request):
    if request.method == 'POST':
        useremail = request.POST.get("email")
        pwd = request.POST.get("password")

        try:
            user = User.objects.get(email=useremail, password=pwd)

            # Check or create subscription
            subscription = Subscription.objects.filter(user=user).first()

            if subscription:
                if subscription.end_date < timezone.now().date():
                    free_plan, _ = Plan.objects.get_or_create(name="Free Plan")  # fallback if missing
                    subscription.plan = free_plan
                    subscription.start_date = timezone.now().date()
                    subscription.end_date = timezone.now().date() + timedelta(days=30)
                    subscription.status = 'active'
                    subscription.pending_credit = 0
                    subscription.save()
            else:
                free_plan, _ = Plan.objects.get_or_create(name="Free Plan")  # handles missing plan
                Subscription.objects.create(
                    user=user,
                    plan=free_plan,
                    start_date=timezone.now().date(),
                    end_date=timezone.now().date() + timedelta(days=30),
                    status='active',
                    pending_credit=0
                )

            # Set session
            request.session['id'] = user.id
            request.session['name'] = user.name
            request.session['email'] = user.email

            return redirect("/index/")

        except User.DoesNotExist:
            messages.error(request, "Invalid Email or Password")
    
    return render(request, "login.html")


    

def signup(request):
    if request.method == "POST":
        f = UserForm(request.POST)

        email = request.POST.get("email")
        mobile_number = request.POST.get("mobile_number")

        # Mobile number validation (10–15 digits only)
        if not re.fullmatch(r'\d{10,15}', mobile_number):
            messages.error(request, "Enter a valid mobile number (10–15 digits).")
            return render(request, "signup.html", {"form": f})

        # Check for existing email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please use another email.")
            return render(request, "signup.html", {"form": f})

        if f.is_valid():
            try:
                user = f.save()

                # Assign FREE plan if available
                free_plan = Plan.objects.filter(name="Free Plan").first()
                if free_plan:
                    start_date = date.today()
                    end_date = start_date + timedelta(days=free_plan.duration_days)

                    Subscription.objects.create(
                        user=user,
                        plan=free_plan,
                        start_date=start_date,
                        end_date=end_date,
                        status='active',
                        pending_credit=free_plan.credit
                    )
                else:
                    print("No free plan found. Please create one in Plan table.")

                messages.success(request, "Signup successful! You can now login.")
                return redirect("/login/")

            except:
                print("----------------------", sys.exc_info())
                messages.error(request, "Something went wrong. Try again later.")
                return render(request, "signup.html", {"form": f})
        else:
            messages.error(request, "Please fix the errors in the form.")
            return render(request, "signup.html", {"form": f})
    else:
        f = UserForm()
        return render(request, "signup.html", {"form": f})
      
def profile(request):
    if 'id' in request.session:
        id = request.session.get('id')
        e = User.objects.get(id=id)
        s = Subscription.objects.filter(user=e.id).first()

        return render(request, 'profile.html',{'e':e,'s':s})

    else:
        return redirect("/login/") 

def update_profile(request, id): 
    e = User.objects.get(id=id)  
    if request.method == "POST":
        f = UserUpdate(request.POST, instance=e)
        if f.is_valid():
            try:
                f.save()
                messages.success(request, "Profile updated successfully.")
            except Exception as ex:
                print("Save error:", ex)
                messages.error(request, "Failed to update profile.")
        else:
            messages.error(request, f"Form validation failed: {f.errors}")
        return redirect('/profile/')
    else:
        return render(request, "updateprofile.html", {'e': e})

def logout(request):
    try:
        request.session.flush()
        return redirect('/login/')
    except:
        pass
    return render(request,'login.html')
def delete_account(request,id):
    if 'id' in request.session:
        e = User.objects.get(id=id)
        e.delete()
        return redirect('/signup/')
    else:
        return render(request,'profile.html')
def forgot(request):
    return render(request,'forgot.html')

def sendotp(request):

    if request.method == "POST":
        otp1 = random.randint(10000, 99999)
        e = request.POST['email']

        request.session['temail']=e

        obj = User.objects.filter(email=e).count()

        if obj == 1:
            
            User.objects.filter(email=e).update(otp=otp1 , otp_used=0)
       
            subject = 'OTP Verification'
            message = str(otp1)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e, ]

            send_mail(subject, message, email_from, recipient_list)

            print("------------mail send---------")
            return render(request, 'set_password.html')
        else:
            messages.error("Invalid email Id")
            return render(request, 'set_password.html')

    else:
        return render(request,"forgot.html")
def set_password(request):
    if request.method == "POST":
        otp = request.POST["otp"]
        pwd = request.POST["new_password"]
        cpwd = request.POST["confirm_password"]
        e =  request.session['temail']

        val = User.objects.filter(email=e,otp=otp,otp_used=0).count()

        if val == 1:
            if pwd == cpwd :
                obj = User.objects.filter(email=e).update(password=pwd,otp_used=1)   
                return redirect("/login/")
            else:
                messages.error(request,"Password and confirm password not match")
                return render(request,"set_password.html")
        else:
            messages.error(request,"Invalid OTP")
            return render(request,"set_password.html") 
def pricing(request) :
    plan_details = Plan.objects.filter(is_active=True)
    return render(request,'pricing.html', {'plans': plan_details})
def features(request):
    return render(request,'features.html')
def blog(request):
    return render(request,'blog.html')
def blogDetails(request):
    return render(request,'blogDetails.html')
def comingsoon(request):
    return render(request,'comingsoon.html')
def contact(request):
    return render(request,'contact.html')
def faq(request):
    return render(request,'faq.html')
def genrate_logo(request):
    if 'id' in request.session:
        category = Category.objects.all()
        return render(request, 'genrate_logo.html', {'category': category})
    else:
        return redirect('/login/')  
from django.utils.timezone import now

def genrateresult_logo(request):
    if 'id' in request.session:
        if request.method == 'POST':
            category_id = request.POST.get('category')
            instruction = request.POST.get('instruction')
            creativity = request.POST.get('creativity')

            user_id = request.session.get('id')
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return redirect('/login/')

            # Subscription check
            subscription = Subscription.objects.filter(
                user=user,
                status='active',
                start_date__lte=now().date(),
                end_date__gte=now().date()
            ).first()

            if not subscription:
                return render(request, "genrateresult_logo.html", {
                    'error': "You do not have an active subscription."
                })

            if subscription.pending_credit <= 0:
                return render(request, "genrateresult_logo.html", {
                    'error': "Your credits are finished. Please renew your plan."
                })

            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                return HttpResponse("Invalid category selected", status=400)

            userprompt = f"{category.name}, {instruction}"

            # Generate image
            try:
                generated_image_object = text2vision(userprompt, creativity, user)
                if not generated_image_object:
                    return render(request, "genrateresult_logo.html", {'messages': "Please try again after sometime."})
            except Exception as e:
                return render(request, "genrateresult_logo.html", {'messages': "Please try again after sometime."})


            # Deduct 1 credit
            subscription.pending_credit -= 1
            subscription.save()


            return render(request, "genrateresult_logo.html", {
                'category': category,
                'instruction': instruction,
                'creativity': creativity,
                'generated_image_url': generated_image_object.image,
                'remaining_credits': subscription.pending_credit
            })

        else:
            return redirect('/genrate_logo/')
    else:
        return redirect('/login/')

def gallery(request):
    if 'id' in request.session:
        user_id = request.session['id']
        user = User.objects.get(id=user_id)
        
        images = Logo.objects.filter(user=user)
        cat = Category.objects.all()
        return render(request, 'gallery.html', {'images': images,'cat':cat})
    else:
        return redirect('/login/')
@csrf_exempt
def paymentsuccessful(request): 
    uid=request.POST.get("id")
    pid=request.POST.get("plan")
    
    print("-----------user id ----------",uid,pid)
    
    p=Plan.objects.get(id=pid)
    sd=date.today()
    ed = sd + timedelta(days=p.duration_days)
    s = Subscription.objects.filter(user=uid).update(plan=pid,start_date=sd,end_date=ed,status='active',pending_credit=p.credit)
    user = User.objects.get(id=uid)
    
    request.session['id'] = user.id
    request.session['name'] = user.name
    request.session['email'] = user.email


    return render (request,'paymentsuccessful.html')
def feedback(request):
    if 'id' in request.session:
        if request.method == "POST":
            comment = request.POST.get("feedback")
            user_id = request.session.get("id")
            user = User.objects.get(id=user_id)
            Feedback.objects.create(user=user, comment=comment)
            return render(request, 'feedback.html', {'feedback_sent': True})  # send flag
        else:
            return render(request, 'feedback.html')
    else:
        return redirect('/login.html/')
def check(request):
    uid = request.session['id']
    s = Subscription.objects.get(user=uid)
    end = s.end_date
    print("--------------------------------------------------------------",end)
    if date.today() >= end:
        logout(request)
        return HttpResponse("YOUR PLAN IS EXPIRED")
    return HttpResponse ("")


     


