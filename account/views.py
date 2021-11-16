from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .forms import (RegisterForm,
                    EditAccountForm, PassForm)


@login_required
def conta(request):
    template_name = 'profile.html'
    return render(request, template_name)


@login_required
def edit_account(request):
    template_name = 'profile_update.html'
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            form = EditAccountForm(instance=request.user)
            context['success'] = True
    else:
        form = EditAccountForm(instance=request.user)
    context['form'] = form
    return render(request, template_name, context)


@login_required
def edit_password(request):
    template_name = 'password_update.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)


def register(request):
    template_name = 'register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                username=user.username, password=form.cleaned_data['password1']
            )
            login(request, user)
            return redirect('core:home')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)


def senha():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(12, chars)


def pass_recovery(request):
    msg = ''
    if request.method == 'POST':
        form = PassForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_404(User, email=email)

            if email == user.email:
                subject = 'Recuperação de senha - E-commerce'
                password = senha()
                user.set_password(password)
                user.save()
                email_from = email
                message = "Olá\nSua nova senha é: "+password
                recipient_list = [email]
                send_mail(subject, message, email_from, recipient_list)
                msg = 'E-mail enviado'
            else:
                msg = 'E-mail ou Usuário inválido'

    form = PassForm()
    return render(request, 'recovery_pass.html',
                  {'form': form, 'msg': msg})