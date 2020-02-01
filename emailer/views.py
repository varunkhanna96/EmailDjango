from django.core.mail import EmailMessage, BadHeaderError
from django.shortcuts import render, HttpResponse, redirect

from emailer import forms
from emailer.exception import exception_handler


def sent(request):
    """
    Response for email sent
    """
    return HttpResponse('Email has been successfully sent.')


@exception_handler(errors=(Exception, ))
def send(request):
    """
    view used to render the email form and to send the email
    """
    if request.method == 'GET':
        form = forms.EmailForm()
    else:
        form = forms.EmailForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = EmailMessage(**data)
            try:
                email.send(fail_silently=False)
            except BadHeaderError as e:
                return HttpResponse('Invalid header found.')
            return redirect('/sent')
    return render(request, "emailer/email_form.html", {'form': form})


def exception(request):
    """
    function to load template to handle all exceptions
    """
    return render(request, 'emailer/exception.html', {})
