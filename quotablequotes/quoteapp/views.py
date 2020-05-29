from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quote
import bcrypt

# Create your views here.
def index(request):
    context = {
        'allUsers': User.objects.all(),
        'allQuotes': Quote.objects.all()
    }
    return render(request, 'index.html', context)

def register(request):
    print(request.POST)
    errors = User.objects.reg_validator(request.POST)
    
    print('errors', errors)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        print('failed to update')
        return redirect('/')
    else:
        securepass = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
        print(securepass)
        newUser = User.objects.create(email = request.POST['email_address'],
                                      password = securepass)
        request.session['loggedinID'] = newUser.id 
        return redirect('/success')

def success(request):
    if 'loggedinID' not in request.session:
        return redirect('/')
    loggedinUser = User.objects.get(id = request.session['loggedinID'])
    context = {
        'loggedin' :loggedinUser
    }
    return render(request, 'success.html', context)

def quotelist(request):
    loggedUser = request.session['loggedinID']
    print('logged in id', loggedUser)
    currentUser = User.objects.get(id= loggedUser).email
    context={
        'allquotes': Quote.objects.all(),
        'loggedId': loggedUser,
        'currentUser': currentUser
    }
    return render(request, 'quotelist.html', context)

def usershow(request, user_id):
    thisUser = User.objects.get(id= user_id)
    userQuotes = thisUser.submitted_quote.all()
    
    context ={
        'thisUser': thisUser,
        'userQuotes':userQuotes,
        'count':userQuotes.count()
    }
    return render(request, 'user.html', context) 

def addQuote(request):
    print(request.POST)
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
            print('failed to add quote')
            return redirect('/quotes')
    else:
        Quote.objects.create( author = request.POST['author'], 
                            message = request.POST['quote'],
                            added_by = User.objects.get(id=request.session['loggedinID']))
        return redirect('/quotes')

def deleteQuote(request, quote_id):
    Quote.objects.get(id=quote_id).delete()
    return redirect('/quotes')

def quoteedit(request, quote_id):
    
    thisQuote = Quote.objects.get(id=quote_id)
    context={
        'thisQuote':thisQuote
    }
    return render(request, 'edit.html', context)

def quoteupdate(request, quote_id):
    print(request.POST)
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
            print('failed to add quote')
            return redirect('/quotes/'+quote_id)
    else:
        thisQuote = Quote.objects.get(id=quote_id)
        thisQuote.author = request.POST['author']
        thisQuote.message = request.POST['quote']
        thisQuote.save()
        messages.success(request, 'quote updated!')
        print('update successful!')
    return redirect('/quotes')

def login(request):
    print(request.POST)
    loginerrors = User.objects.login_validator(request.POST)
    print(loginerrors)
    if len(loginerrors) > 0:
        for key, value in loginerrors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        loggedUser = User.objects.filter(email = request.POST['login_email'])[0]
        print('printin a list of user objects that match the login form')
        print('loggedUser', loggedUser)
        request.session['loggedinID'] = loggedUser.id 
        return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')