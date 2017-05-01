from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'wd2csv/index.dtl', context)
