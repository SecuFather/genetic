from django.shortcuts import render
from genetic.func import Genetic


def index(request):
    context = {}
    if request.method == 'POST':
        Genetic().start(request.POST)
        context = request.POST

    return render(request, 'index.html', context)