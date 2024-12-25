from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

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


def dashboard_view(request):
    user = request.user
    context = {
        'user': user,
    }

    return render(request, 'pages/user_profile.html', context)
