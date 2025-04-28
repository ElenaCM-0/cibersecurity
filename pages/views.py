from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.template import Template, Context
import sqlite3

import requests

from pages.forms import minipageForm
from pages.models import minipage

context = {'pages': False}

# Create your views here.
def init(request):
	return render(request, 'pages/index.html')

def snippet(request):
	if request.method != 'GET':
		return redirect('/')
	
	target_page = request.GET.get('target')

	response = requests.get(target_page)

	return HttpResponse(response.content.decode[:300])

def createUser(request):
	# Create user
	if request.method != 'POST':
		return redirect('/')
	
	username = request.POST.get('username')
	password = request.POST.get('password')

	if User.objects.filter(username=username).exists():
		return redirect('/login', message="The username is already in use, try a different one!")

	new_user = User.objects.create_user(username=username, password=password)

	# Fix password thing

	login(request, new_user)

	return render(request, 'pages/index.html')

def page(request, name):
	if request.method != 'GET':
		return redirect('/')

	if not minipage.objects.filter(name=name).exists():
		return HttpResponse("The given name does not correspond to any page!")

	page = minipage.objects.get(name=name)

	template = Template("<h1>" + page.name + " </h1>" + "{{ content|linebreaks }}")
	context = Context({"content": page.content})
	
	return HttpResponse(template.render(context))

@login_required
def homePage(request):
	# Visual of all of the user's pages
	pages = minipage.objects.filter(owner = request.user)

	# if this is a POST request, process the form data
	if request.method == "POST":
        # create a form instance and populate it with data from the request:
		form = minipageForm(request.POST, user=request.user)
		
		if form.is_valid():
			form.save()
		
	else:
		form = minipageForm(user=request.user)

	return render(request, 'pages/home.html', {'pages': pages, 'createPageForm': form})
	

def search(request):
	key = request.POST.get('key')

	# Find page in database

	conn = sqlite3.connect('db.sqlite3').cursor()
	
	pages = conn.execute("SELECT * FROM minipage WHERE name LIKE '%" + key + "%'")

	# pages = minipage.objects.filter(name__contains=key) 

	# Render the appropiate page
	return render(request, 'pages/index.html', {'pages': pages})