from django.shortcuts import render
from gif import models

# Create your views here.
Num = 1
def index(request):
    v1 = models.gif_init.objects.all().values('name', 'url')
    c = auto_value(v1)
    if request.method == "GET":
        v2 = c.__next__()
        # v2 = models.UserInfo.objects.get(id=num)
        # return render(request,"login.html")
    if request.method == "POST":
        global Num
        Num += 1
        for i in range(Num):
            v2 = c.__next__()
    return render(request, "index.html",{"v2":v2})


def auto_value(v1):
    for i in v1:
        yield i

def login(request):
    v1 = models.gif_init.objects.all().values('name', 'url')
    return render(request, "login.html",{"v1":v1})