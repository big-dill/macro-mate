from django.shortcuts import render


# Create your views here.

def index(request):
    context_dict = {}
    response = render(request, 'macro_mate/index.html', context=context_dict)
    return response


def meals(request):
    context_dict = {}
    response = render(request, 'macro_mate/meals.html', context=context_dict)
    return response


def weekly_plan(request):
    context_dict = {}
    response = render(request, 'macro_mate/weekly_plan.html', context=context_dict)
    return response
