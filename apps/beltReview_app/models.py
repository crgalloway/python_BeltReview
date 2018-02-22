# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
# NAME_REGEX

class userManager(models.Manager):
	def userValidate(self,postData):
		response = {
			'status': True
		}
		errors = []
		if len(postData['name']) == 0 or len(postData['alias']) == 0 or len(postData['email']) == 0 or len(postData['password1']) == 0:
			errors.append("All fields are required")
		if len(postData['name']) < 2:
			errors.append("Name is too short")
		# NAME REGEX GOES HERE
		if len(postData['alias']) < 2:
			errors.append("Alias name is too short")
		if len(postData['password1']) < 8:
			errors.append("Password is too short")
		if postData['password1'] != postData['password2']:
			errors.append("Password confirmation must match")
		if not EMAIL_REGEX.match(postData['email']):
			errors.append("Must be a valid e-mail")
		response['email'] = user.objects.filter(email=postData['email'])
		if len(response['email']) > 0:
			errors.append("Must be a valid e-mail")
		if len(errors) > 0:
			response['status'] = False
		else:
			hashedPw = bcrypt.hashpw(postData['password1'].encode(), bcrypt.gensalt())
			response['user'] = user.objects.create(name=postData['name'],alias=postData['alias'],email=postData['email'],password=hashedPw)
		response['errors'] = errors
		return response
	def loginValidate(self,postData):
		response = {
			'status': True,
			'login': user.objects.filter(email=postData['email'])
		}
		if len(response['login']) == 1 and bcrypt.checkpw(postData['password1'].encode(), response['login'][0].password.encode()):
			response['user'] = response['login'][0]
		else:
			response['status'] = False
		return response

class booksManager(models.Manager):
	def bookValidate(self,postData,activeUser):
		response = {
			'status': True,
			'uploaded_by': user.objects.get(id=activeUser)
		}
		errors = []
		response['title'] = book.objects.filter(title=postData['title'])
		if len(response['title']) > 0:
			errors.append("Book already in system, please leave a <a href='/books/"+str(response['title'][0].id)+"'>review</a> instead")
		if len(postData['authorText']) > 0:
			author = postData['authorText']
		else:
			author = postData['authorMenu']
		if len(postData['title']) == 0 or len(author) == 0:
			errors.append("All fields are required")
		if len(errors) > 0:
			response['status'] = False
		else:
			response['book'] = book.objects.create(title=postData['title'],author=author,uploaded_by=response['uploaded_by'])
		response['errors'] = errors
		return response

class reviewsManager(models.Manager):
	def reviewValidate(self,postData,book,activeUser):
		response = {
			'status': True,
			'left_by': user.objects.get(id=activeUser)
		}
		errors = []
		if len(postData['comment']) == 0:
			errors.append("All fields are required")
			response['status'] = False
		response['review'] = review.objects.create(review_of=book,left_by=response['left_by'],comment=postData['comment'],rating=postData['rating'])
		response['errors'] = errors
		return response

class user(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = userManager()

class book(models.Model):
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	uploaded_by = models.ForeignKey(user, related_name="uploaded")
	objects = booksManager()

class review(models.Model):
	review_of = models.ForeignKey(book, related_name="has_review")
	left_by = models.ForeignKey(user, related_name="left_review")
	comment = models.CharField(max_length=255)
	rating = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = reviewsManager()