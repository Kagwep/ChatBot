from email import message
from multiprocessing import context
from django.shortcuts import render

from.models import Video
from json import dumps


def response(request):
    video = Video.objects.all()
    context ={"video":video}
    return render(request, "index.html", context)


    

