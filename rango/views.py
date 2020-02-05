from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page


def index(request):#calls your main page
    #context dictionary hopefully holds keys for the {{}} in your template
    category_list = Category.objects.order_by('-likes')[:5]
    pages = Page.objects.order_by('-views')[:5]
    #first five tallest likes
    context_dict={}
    context_dict['boldmessage']='Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories']=category_list
    context_dict['pages']=pages
    #render the appropriate template
    
    return render(request,'rango/index.html',context=context_dict)
    

def about(request):
    context_dict={'boldmessage':  'This tutorial has been put together by ACM.' }
    #render the appropriate template
    return render(request,'rango/about.html',context=context_dict)
    
def show_category(request, category_name_slug):
# Create a context dictionary which we can pass
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages']=pages
        context_dict['category']=category
    except Category.DoesNotExist:
        context_dict['pages']=None
        context_dict['category']=None
    return render(request, 'rango/category.html', context=context_dict)