from django.shortcuts import render
from .models import Player, Focus
# Create your views here.
from django.http import HttpResponse


def focustable(request):
    focuses = Focus.objects.all()
    slyakot = 666
    context = {'slyakot': slyakot,
                'focuses':focuses}
    return render(request, 'trust/focus.html', context)
