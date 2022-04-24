from email import message
from multiprocessing import context
from django.shortcuts import render

from.models import Video
from json import dumps
from django.db.models import Q


def response(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    videos = Video.objects.filter(
        Q(title__icontains = q) 
 
        )

    context ={"videos":videos}
    return render(request, "index.html", context)
def ViewTurorial(request,pk):
    video = Video.objects.get(id = pk)
    context = {'video':video}
    return render(request, 'home.html', context)

    

