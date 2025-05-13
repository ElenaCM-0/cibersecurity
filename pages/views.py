from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.template import Template, Context
import sqlite3

from pages.forms import minipageForm
from pages.models import minipage

# Create your views here.
def init(request):
	pages = minipage.objects.filter()
	return render(request, 'pages/index.html', {"pages": pages})

def newAccount(request):
	return render(request, 'pages/newAccount.html', {"form" : UserCreationForm()}) #1.3

	# return render(request, 'pages/newAccount.html') # #1.3 begin and end

def createUser(request):
	# #1.2
	# if request.method != 'POST':
	# 	return redirect('/')
	# 
	# form = UserCreationForm(request.POST)
	# 
	# # Validate password
	# 
	# if not form.is_valid(): #2
	# 	return render(request, 'pages/newAccount.html', {"form" : form})
	# 
	# new_user = form.save()
	# 
	# login(request, new_user)
	# 
	# return render(request, 'pages/index.html')

	# #1.2 begin
	# Create user

	if request.method != 'GET':
		return redirect('/')
	
	username = request.GET.get('username')
	password = request.GET.get('password')

	if User.objects.filter(username=username).exists():
		return redirect('/login', message="The username is already in use, try a different one!")

	new_user = User.objects.create_user(username=username, password=password)

	login(request, new_user)

	return redirect('/')
	# #1.2 end

def page(request, name):
	if request.method != 'GET':
		return redirect('/')

	if not minipage.objects.filter(name=name).exists():
		return HttpResponse("The given name does not correspond to any page!")

	page = minipage.objects.get(name=name)

	template = Template("<h1> {{name}} </h1>" + "{{ content|linebreaks }}" + "<a href='/'> <button>Back to start</button> </a>")
	context = Context({"content": page.content, "name" : page.name})
	
	return HttpResponse(template.render(context))

@login_required
def deletePage(request, name):
	if request.method != 'POST':
		return redirect('/')
	
	if not request.user.is_superuser:
		return redirect('/')

	if not minipage.objects.filter(name=name).exists():
		return HttpResponse("The given name does not correspond to any page!")

	minipage.objects.get(name=name).delete()
	
	return redirect('/')

# @login_required #4.1
def homePage(request, username):
	# Visual of all of the user's pages
	user = User.objects.get(username=username) #4.2 begin and end
	# #4.2 user = request.user

	# #5.2
	# if user.is_superuser:
	#	return adminPage(request) 

	pages = minipage.objects.filter(owner = user)

	# if this is a POST request, process the form data
	if request.method == "POST":
        # create a form instance and populate it with data from the request:
		form = minipageForm(request.POST, user = user)
		
		if form.is_valid():
			form.save()
			form = minipageForm(user = user)
		
	else:
		form = minipageForm(user = user)

	return render(request, 'pages/home.html', {'pages': pages, 'createPageForm': form})

def adminPage(request):
	users = User.objects.filter(is_superuser = False)

	user_pages = {}

	for u in users:
		user_pages[u] = minipage.objects.filter(owner = u)

	return render(request, 'pages/admin.html', {'users': user_pages})
	

def search(request):
	key = request.POST.get('key')

	if not key:
		return redirect('/')

	# Find page in database


	# #3.1 begin

	conn = sqlite3.connect('db.sqlite3').cursor()
	
	pages = conn.execute("SELECT * FROM minipage WHERE name LIKE '%" + key + "%'")
	size = pages.rowcount

	# #3.1 end

	# #3.1
	# pages = minipage.objects.filter(name__contains=key) 
	# size = len(pages)

	# Render the appropiate page
	if size <= 0:
		return render(request, 'pages/index.html', {'no_results': True, 'query': key})

	return render(request, 'pages/index.html', {'pages': pages})