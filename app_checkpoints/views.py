from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from django.template.defaultfilters import register
from num2words import num2words


@register.filter
def to_words(value, lang='en'):
    return num2words(value, lang=lang)



@require_http_methods(["GET"])
def home(request):
    return render(request, 'home.html')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')