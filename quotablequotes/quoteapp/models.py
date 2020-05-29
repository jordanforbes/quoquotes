from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    def reg_validator(self, post_data):
        print('validator time')
        print('post data: ', post_data)
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(post_data['email_address']) == 0:
            errors['emailrequired'] = 'email cannot be empty'
        elif not EMAIL_REGEX.match(post_data['email_address']):
            errors['emailwrong'] = 'invalid email'
        if len(post_data['pw'])< 8:
            errors['pw'] = 'password must be at least 8 chars'
        if post_data['pw'] != post_data['confpw']:
            errors['confpw'] = 'password must match confirmation'
        return errors

    def login_validator(self, post_data):
        print('login_validator, below is the post data')
        print(post_data)
        errors = {}
        if len(post_data['login_email']) == 0:
            errors['emailrequired'] = 'Email is required'
        else:
            usersWithEmail = User.objects.filter(email = post_data['login_email'])
            if len(usersWithEmail) == 0:
                errors['emailnotregistered'] = 'email not found'
            else:
                usertocheck = usersWithEmail[0]
                if bcrypt.checkpw(post_data['login_pw'].encode(), usertocheck.password.encode()):
                    print('password matches')
                else:
                    errors['pwwrong'] = 'password is incorrect'
        return errors

class QuoteManager(models.Manager):
    def quote_validator(self, post_data):
        print('validation')
        print('post data',post_data)
        errors={}
        if len(post_data['author']) < 2:
            errors['invalidauthor'] = 'author must be at least 2 characters'
        if len(post_data['quote']) < 10:
            errors['invalidquote'] = 'quote must be at least 10 characters'
        return errors
            
class User(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True) 
    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length = 255)
    message = models.CharField(max_length = 255)
    added_by = models.ForeignKey(User, related_name="submitted_quote", on_delete= models.CASCADE)
    favorites = models.ManyToManyField(User, related_name="favorite_quote")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = QuoteManager()
# Create your models here.
