from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    context = {}
    return render(request, 'index.dtl', context)


@login_required()
def profile(request):
    context = {}
    return render(request, 'profile.dtl', context)


def login_oauth(request):
    context = {}
    return render(request, 'login.dtl', context)
