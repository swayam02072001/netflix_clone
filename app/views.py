import re
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib import auth
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.
@login_required(login_url='/')
def index(request):
    gen=Genre.objects.all()
    movies = Movie.objects.all()
    context = {'movies':movies,'genre':gen}
    return render(request,'index.html',context)


def add_to_list(request):
    if request.method == 'POST':
        movie_url_id = request.POST.get('movie_id')
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        match = re.search(uuid_pattern,movie_url_id)
        print(match)
        movie_id = match.group() if match else None
        print(movie_id)
        movie = get_object_or_404(Movie,uu_id=movie_id)
        print(movie)
        movie_list, created = Movielist.objects.get_or_create(owner_user=request.user,movie=movie) 
        movie_list.save()     
        if created:
            response_data = {'status':'success','message':'Added'}
        else:
            response_data = {'status':'info','message':'Movie already in list'}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'status':'error','message':'Invalid request'},status=400)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None: 
            auth.login(request,user)
            return redirect('/index')
        else:
            messages.info(request,'Credentials Invalid !!')
            return redirect('/')
    return render(request,'login.html')

@login_required(login_url='/')
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='/')
def movie(request,pk):
    movie_uuid = pk
    gen = Genre.objects.all()
    movie_details = Movie.objects.get(uu_id=movie_uuid)
    context = {'movie_details':movie_details,'genre':gen}

    return render(request,'movie.html',context)


def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email alrady taken')
                return redirect('/signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username alrady taken')
                return redirect('/signup')
            else:
                user =User.objects.create_user(username=username,email=email,password=password)
                user.save()
                
                return redirect('/')
                
        else:
            messages.info(request,'Password is Not Matching')
            return redirect('/signup')
        
    else:
        return render(request,'signup.html')



@login_required(login_url='/')
def my_list(request):
    gen = Genre.objects.all()
    MO = Movielist.objects.filter(owner_user=request.user)
    AMO = []
    for i in MO:
        AMO.append(i.movie)
   
    return render(request,'my_list.html',{'movies':AMO,'genre':gen})

@login_required(login_url='/')
def search(request):
    gen = Genre.objects.all()
    if request.method == 'POST':
        search_term = request.POST['search_term']
        movies = Movie.objects.filter(title__icontains=search_term)
        context = {'movies':movies,"search_term":search_term,'genre':gen}
    
        return render(request,'search.html',context)
    else:
        return redirect('app/index',{'genre':gen})

@login_required(login_url='/')
def genre(request,pk):
    movie_genre = pk
    gen = Genre.objects.all()
    movies = Movie.objects.filter(genre=movie_genre)
    context = {'movies':movies,"movie_genre":movie_genre,'genre':gen}
    return render(request,'genre.html',context)