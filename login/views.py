from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse  # Http404
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import views
#from django.utils import simplejson
#import json
#from django.core.context_processors import csrf

from django.views.decorators.csrf import csrf_protect

#from django.core.mail import send_mail

#from django.core.urlresolvers import reverse, resolve

from django.contrib.auth.views import (password_reset, password_reset_complete,
                                       password_reset_confirm)

from register.models import User_Data
from login.forms import LoginForm, PasswordResetForm, ChangePasswordForm


def dummy_ajax(request):
    print "I called dummy, ajax after blur from username field on form."
    return HttpResponse("OK")


@csrf_protect
def ajax_login_username_check(request):
    #c = {}
    #c.update(csrf(request))

    if request.method == 'GET' and request.GET['u']:
        searchfor = request.GET['u']

        try:
            u = User.objects.get(username=searchfor)
            print('Successfully accomplished query.')
            print(u.last_name)

        except User.DoesNotExist:
            print('There is NO such user name')
            #c = {'check': 'Error', }
            return HttpResponse('ERR')

    #c = {'check': 'OK', }
    return HttpResponse('OK')
    #return HttpResponse(c)


def process_login(request):
    """
    View function for loging in a site.
    """
    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():
            #return HttpResponse('THE FORM IS VALID!')
            #return HttpResponse(form.cleaned_data['username'])
            # Assigning & clearing input values.
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #return HttpResponse('username is: %s' % username)
            #return HttpResponse('password is: %s' % password)

            # Checking username with database username value.
            #return HttpResponse('AUTHENTICATING!')
            user = auth.authenticate(username=username, password=password)
            #return HttpResponse('AUTHENTICATED!')
            #return HttpResponse('user is: %s' % user)

            if user is not None and user.is_active:
                #return HttpResponse('TRYING TO LOGIN!')
                auth.login(request, user)
                #return HttpResponse('LOGGED IN!')
                return HttpResponseRedirect('/login/loged-in/')

            else:
                return HttpResponseRedirect('/login/login-error/')

    else:
        form = LoginForm()  # An unbound form.

    context = {
        'form': form,
        'formname': 'Login',
    }

    return render_to_response('login/login-index.html',
                              context,
                              context_instance=RequestContext(request))


def process_logout(request):
    auth.logout(request)

    return HttpResponseRedirect('/login/loged-out/')


def forgot_password_context_processor(request):
    return {
        'formname2': 'Forgot Password',

    }


def forgot_password(request):
    context = {}
    return render_to_response(
        'login/forgot_password.html',
        context,
        context_instance=RequestContext(request))


@csrf_protect
def password_reset(request):
    """
    This uses password-reset-request url name.
    """
    template_response = views.password_reset(request,
                                             template_name='login/password_reset_form.html',
                                             email_template_name='login/password_reset_email.html',
                                             post_reset_redirect='login:password_reset_done',
                                             password_reset_form=PasswordResetForm)

    return template_response


def password_reset_done(request):
    """
    The page  shown after a user has been emailed a link to reset their password.
    This view is called after email with a link  was sent to the user.
    Returns template response too.
    """
    template_response = views.password_reset_done(request,
                                                  template_name='login/password_reset_done.html')

    return template_response


#def password_reset_confirm(request):
#    """
#    password_reset_confirm function is used from django.
#    This function presents a form for entering a new password.
#    """
#    template_response = views.password_reset_confirm(request,
#                                                     token_generator=default_token_generator,
#
#                                                    )

#"""
#password_reset_complete.
#Presents a view which informs the user that the password has been successfully changed.
#"""

def password_reset_succesfully_changed(request):
    pass


def loged_in(request):
    #path = User_Data.objects.get()
    context = {}

    return render_to_response('login/you_are_loged_in.html',
                              context,
                              context_instance=RequestContext(request))


def loged_out(request):
    context = {}

    return render_to_response('login/you_are_loged_out.html',
                              context,
                              context_instance=RequestContext(request))


def error_login(request):
    context = {}

    return render_to_response('login/wrong_username_or_password.html',
                              context,
                              context_instance=RequestContext(request))


def show_portrait(request):
    """
    Provide a link to a picture of the current user.
    """
    if request.user.is_authenticated():
        # query the portrait end part from db.
        user = User_Data.objects.get(user=request.user.id)

        if user.portrait.url:
            portpath = user.portrait.url
            context = {'portpath': portpath}

            return render_to_response('login/show_portrait.html',
                                      context,
                                      context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/no/available/portrait/')


def no_portrait(request):
    context = {}
    return render_to_response('login/no_portrait.html',
                              context,
                              context_instance=RequestContext(request))
