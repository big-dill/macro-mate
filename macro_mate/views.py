from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect 
from macro_mate.models import UserProfile


# Create your views here.


def index(request):
    context_dict = {}
    response = render(request, 'macro_mate/index.html', context=context_dict)
    return response

def user_login(request):
    # pulling the relevant login information
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password = password)

        # if the login details are correct 
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('macro_mate:index'))
            else:
                return HttpResponse("Your MacroMate account is disabled.")
        else:
            print("Incorrect login details: {username}, {password}")
            return HttpResponse("Incorrect login details")
    else:
        return render(request, 'macro_mate/login.html')

