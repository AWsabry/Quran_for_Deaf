from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from Quran_for_Deaf import settings
from users.models import CustomUser, AccessToken
from django.contrib.auth.decorators import login_required
from users.decorators import auth_users_not_access
from users.forms import CustomUserForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate
from users.utils import AccessTokenGenerator
from users.thread import EmailThread
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage

# Create your views here.

def send_tracking(user):
    user = CustomUser.objects.filter(id=user.id).first()
    last_token = user.token.filter(user=user, expires__gt=timezone.now()).first()
    if not last_token:
        access_token = user.token.create(user=user)
        return (access_token.token, 0)
    return (False, (last_token.expires - timezone.now()).total_seconds())

def token_check(user):
    token, time_tosend = send_tracking(user=user)
    if token:
        return (token,time_tosend)
    return (None,time_tosend)

def send_activate_mail(request, user):  
        token, time_tosend = token_check(user)
        if token:
            domain = get_current_site(request)
            subject = _('Activate user account')
            body = render_to_string('activate.html', {
                'user':user,
                'domain':domain,
                'token':token,
            })
            email = EmailMessage(subject, body, settings.EMAIL_HOST_USER, [user.email])
            email.send()
            # EmailThread(subject, body, [user.email]).start()
            messages.success(request, _('There are an mail has been sent.'))
        else:
            messages.error(request,_('Please varify the account (an email have been sent) please wait %(time_tosend)8.0f') % {'time_tosend':time_tosend} , extra_tags='danger')

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        email = form.data.get('email')
        first_name, last_name = form.data.get('first_name'), form.data.get('last_name')
        password = form.data.get('password1')
        country = form.data.get('country')
        
        if form.is_valid():
            user = CustomUser.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                country=country
            )
            send_activate_mail(request, user)
            return redirect('login')
        else:
            messages.error(request, _('This showing something wrong!'), extra_tags='danger')
    else:
        form = CustomUserForm()
        
    return render(request, 'sign_up.html', {'form':form})

@csrf_exempt
def login(request):
    if request.method == 'POST' and 'login_btn' in request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            if user.is_active:
                print('active')
                return redirect('Deaf_Website:index')
            else:
                send_activate_mail(request, user)
                return redirect('login')
        else:
            messages.error(request, _('There are some wrong infomation try again'), extra_tags='danger')
            return redirect('login')
    return render(request, 'login.html')

def activate_user(request, token):
    token = AccessToken.objects.filter(token=token).first()
    
    if token:
        last_token = AccessToken.objects.filter(user=token.user, expires__gt=timezone.now()).first()
        if last_token == token:
            if AccessTokenGenerator().check_token(token.user, token.token):       
                token.user.is_active = True
                token.user.save()
                messages.success(request, 'لقد تم تفعيل الحساب يمكنك تسجيل الدخول الآن')
            else:
                messages.error(request, 'تم تفعيل هذا الحساب مسبقا', extra_tags='danger')
        else:   
            messages.error(request, 'لقد انتهى الوقت المسموح لهذا الرابط', extra_tags='danger')
    else:
        messages.error(request, 'لم نتمكن من ايجاد هذا الرابط، حاول مرة اخرى', extra_tags='danger')
    
    return redirect('login')
