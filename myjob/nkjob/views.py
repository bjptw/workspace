from django.shortcuts import render
from nkjob import models

# Create your views here.
def index(request):
    v1 = models.position_51.objects.all().values('up_time', 'position','pay','addr', 'name','url')
    return render(request,"index.html",{"v1":v1})