from django.shortcuts import render

# Create your views here.


def index(request):
    context_dict = {}
    response = render(request, 'macro_mate/index.html', context=context_dict)
    return response

def login(request):
    context_dict = {}
    response = render(request, 'macro_mate/login.html', context=context_dict)
    return response



