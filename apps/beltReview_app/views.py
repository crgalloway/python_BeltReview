# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import user, book, review

def index(request):
	return render(request, 'beltReview_app/index.html')

def register(request):
	response = user.objects.userValidate(request.POST)
	if len(response['errors']) < 1:
		request.session['activeUser'] = response['user'].id
		return redirect('/books')
	else:
		for error in response['errors']:
			messages.error(request, error)
		return redirect('/')

def login(request):
	response = user.objects.loginValidate(request.POST)
	if response['status']:
		request.session['activeUser'] = response['user'].id
		return redirect('/books')
	else:
		messages.error(request,"Invalid email/password combination")
		return redirect('/')

def books(request):
	if not 'activeUser' in request.session:
		messages.error(request,"You must be logged in")
		return redirect('/')
	query = user.objects.get(id=request.session['activeUser'])
	context = {
		'userAlias': query.alias,
		'recentReviews': review.objects.all().order_by('-created_at')[:3],
		'reviewList': review.objects.raw('SELECT * FROM beltReview_app_review JOIN beltReview_app_book ON beltReview_app_book.id = review_of_id GROUP BY title')
	}
	temp1 = review.objects.all()
	temp2 = ""
	return render(request, 'beltReview_app/home.html',context)

def logout(request):
	request.session.clear()
	return redirect('/')

def add(request):
	if not 'activeUser' in request.session:
		messages.error(request,"You must be logged in")
		return redirect('/')
	context = {
		'authorList': book.objects.raw("SELECT * FROM beltReview_app_book GROUP BY author")
	}
	return render(request, 'beltReview_app/add.html',context)

def processAdd(request):
	bookResponse = book.objects.bookValidate(request.POST,request.session['activeUser'])
	if not bookResponse['status']:
		for error in bookResponse['errors']:
			messages.error(request, error)
		return redirect('/books/add')
	reviewResponse = review.objects.reviewValidate(request.POST,bookResponse['book'],request.session['activeUser'])
	if not reviewResponse['status']:
		for error in reviewResponse['errors']:
			messages.error(request, error)
		return redirect('/books/add')
	return redirect('/books/'+str(bookResponse['book'].id))

def processReview(request):
	bookObj = book.objects.get(id=request.POST['bookID'])
	reviewResponse = review.objects.reviewValidate(request.POST,bookObj,request.session['activeUser'])
	return redirect('/books/'+str(request.POST['bookID']))

def users(request,number):
	if not 'activeUser' in request.session:
		messages.error(request,"You must be logged in")
		return redirect('/')
	context = {
		'user': user.objects.get(id=number),
		'count': user.objects.get(id=number).left_review.count(),
		'reviews': user.objects.get(id=number).left_review.all()
	}
	return render(request,'beltReview_app/user.html',context)

def bookInfo(request,number):
	if not 'activeUser' in request.session:
		messages.error(request,"You must be logged in")
		return redirect('/')
	context = {
		'book': book.objects.get(id=number),
		'reviews': book.objects.get(id=number).has_review.all()
	}
	return render(request,'beltReview_app/book.html',context)

def destroy(request,number):
	if not 'activeUser' in request.session:
		messages.error(request,"You must be logged in")
		return redirect('/')
	bookID = review.objects.get(id=number).review_of.id
	review.objects.get(id=number).delete()
	return redirect('/books/'+str(bookID))