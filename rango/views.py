from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    #context dictionary hopefully holds keys for the {{}} in your template
    context_dict={'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    #render the appropriate template
    return render(request,'rango/index.html',context=context_dict)
# Create your views here.
def about(request):
    context_dict={'boldmessage':  'This tutorial has been put together by ACM.' }
    #render the appropriate template
    return render(request,'rango/about.html',context=context_dict)