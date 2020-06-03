from django.shortcuts import render
from .models import Blogpost
# Create your views here.
from django.http import HttpResponse

# Create your views here.
def index(request):
    mypost=Blogpost.objects.all()
    return render(request, 'blog/index.html',{'mypost':mypost})

def blogpost(request,id):
    post=Blogpost.objects.filter(post_id=id)[0]
    return render(request, 'blog/blogpost.html',{'post':post})