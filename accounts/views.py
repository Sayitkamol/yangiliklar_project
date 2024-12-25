from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import LoginForm, UserRegistrationForm

""" Login view """
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request=request, username=data['username'], password=data['password'])
            # print(data, user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Login Muvaffaqiyatli!')
                else:
                    return HttpResponse('Sizning profilingiz faol emas!')
            else:
                return HttpResponse('Login yoki parolda xatolik bor!')

    form = LoginForm()
    context = {'form': form}

    return render(request, 'registration/login.html', context=context)

""" Logout view """
def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html') # Replace 'login' with the name of your login page URL

""" Dashboard View """
def dashboard_view(request):
    user = request.user
    context = {
        'user': user,
    }

    return render(request, 'pages/user_profile.html', context)


""" Signup view """
''' 1-usul '''
def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            context = {
                'new_user': new_user,
            }
            return render(request, 'account/register_done.html',context)
    else:
        user_form = UserRegistrationForm()
        context = {
            'user_form': user_form,
        }
        return render(request, 'account/register.html', context)

''' 2-usul '''
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'account/register.html'

''' 3-usul '''
class SignUpVeiw2(View):

    def get(self, request):
        user_form = UserRegistrationForm()
        context = {
            'user_form': user_form,
        }
        return render(request, 'account/register.html', context)

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            context = {
                'new_user': new_user,
            }
            return render(request, 'account/register_done.html',context)