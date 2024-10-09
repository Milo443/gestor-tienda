from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .form import RegistrationForm, LoginForm
from .models import Token

# Create your views here.
def inicio(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            new_token = get_random_string(length=6, allowed_chars='0123456789')
            Token.objects.create(user=user, token=new_token)
            send_mail(
                'Your login token',
                f'Your login token is {new_token}',
                'cakes98otaku@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect('verify_token', email=email)
    return render(request, 'login.html')

def verify_token(request, email):
    if request.method == 'POST':
        token = request.POST.get('token')
        user = User.objects.filter(email=email).first()
        if user:
            token_obj = Token.objects.filter(user=user, token=token).first()
            if token_obj:
                token_obj.delete()
                # Log in the user
                return redirect('main')
    return render(request, 'verify_token.html', {'email': email})


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        if email and username:
            user, created = User.objects.get_or_create(username=username, email=email)
            if created:
                user.set_unusable_password()
                user.save()
            token = get_random_string(length=6, allowed_chars='0123456789')
            Token.objects.create(user=user, token=token)
            send_mail(
                'Your login token',
                f'Your login token is {token}',
                'cakes98otaku@gmail.com',
                [email],
                fail_silently=False,
            )
            print(f"Email sent to {email} with token {token}")  # Mensaje de depuración
            return redirect('login')
        else:
            print("Email or username not provided")  # Mensaje de depuración
    else:
        print("GET request received")  # Mensaje de depuración
    return render(request, 'register.html')



#main

def main(request):
    return render(request, 'main.html')