from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)
    return render(request, 'rango/about.html', {})
    
@login_required     
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
    # Now that the category is saved, we could confirm this.
    # For now, just redirect the user back to the index view.
            return redirect('/rango/')
        else:
            print(form.errors)
            
    return render(request, 'rango/add_category.html', {'form': form})
@login_required    
def add_page(request, category_name_slug):
    try :
        category= Category.objects.get(slug=category_name_slug)
    except:
        category=None
    
    if category is None:
        return redirect('/rango/')
        
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page=form.save(commit=False) #hm. Must be checks.
                page.category = category
                page.views = 0
                page.save()
                
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
                #reverse looks up URLS from show_category. As we're using that, we also need to mess with slugs.
        else:
            print(form.errors)
    context_dict={'form':form, 'category':category}
    return render(request, 'rango/add_page.html', context=context_dict)
    
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
    
def register(request):
    registered=False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)#SQL likes all data at once plz. Otherwise FK errors.
            profile.user=user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
            registered= True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form= UserForm()
        profile_form = UserProfileForm()
        
    return render(request,'rango/register.html', context = {'user_form': user_form,'profile_form': profile_form, 'registered': registered})
    #both forms and wheter the registration went through
def user_login (request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied")
            
    else:#invalid request or a poorly made spoof
        return render(request, 'rango/login.html')
        
@login_required        
def restricted(request):
    return render(request, 'rango/restricted.html')
    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))