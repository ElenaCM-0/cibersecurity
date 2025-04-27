from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
import sqlite3

from pages.models import minipage

context = {'pages': False}

# Create your views here.
def init(request):
	return render(request, 'pages/index.html')

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

@login_required
def homePage(request):
	# Create page button

	# Visual of all of the user's pages
	pages = minipage.objects.filter(owner = request.user)

	return render(request, 'pages/home.html', {'pages': pages})

def search(request):
	key = request.POST.get('key')

	# Find page in database

	conn = sqlite3.connect('db.sqlite3').cursor()
	
	pages = conn.execute("SELECT * FROM minipage WHERE name LIKE '%" + key + "%'")

	# pages = minipage.objects.filter(name__contains=key) 

	# Render the appropiate page
	return render(request, 'pages/index.html', {'pages': pages})