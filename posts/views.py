from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, \
    get_object_or_404  # get_object_or_404() is a Django shortcut function that helps you fetch a single object from the database safely.
# It tries to get an object. If it exists — great, you get the object. If it doesn’t — Django automatically raises a 404 Not Found error.
# This will crash your app if the object doesn't exist
# tweet = Tweets.objects.get(id=5)
from posts.models import Tweets
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
import django.contrib.auth
from django.contrib.auth import authenticate
from django.urls import reverse # for HttpResponseRedirect

def homepage(request):  # To view all tweets on the homepage we need to fetch tweets from the database and display it on homepage.
    tweets = Tweets.objects.all().order_by('-created_at')  # Or filter by user
    return render(request, "index.html", {'tweets': tweets})


def register(request):
    if request.method == "POST":
        name = request.POST.get('username')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')

        if pass1 != pass2:
            messages.error(request, "Passwords Don't match")
            return redirect('register')  # name of the url is passed.

        if User.objects.filter(username=name).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        user = User.objects.create_user(username=name, password=pass1)
        user.save()
        messages.success(request, "Account created successfully. You can now log in.")
        return redirect('login_form')

    return render(request, "registrations/register.html")  # As the registration is not in the templates folder directly so mention sub-folder and then html page.


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)  #This is incorrect because Django’s authenticate() does not accept email

        if user is not None:
            django.contrib.auth.login(request, user)  # ✅ No more confusion. # This is Django’s built-in login() function, imported from from django.contrib.auth import authenticate, login
            return redirect('index')  # Use the name you gave in your urls.py
        # return HttpResponseRedirect(reverse('login_form')) if use Httpresposeredirrect
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login_form')

    return render(request, "registrations/login_form.html")


@login_required
def logout_view(request):
    logout(request)  # Django built-in function
    return redirect('login_form')


@login_required
def create_tweet(request):
    # context = {} # It's defined here as empty dictionary b/c: when the request method != POST, then it can render it with empty dictionary (data passed to html page)

    return render(request, "tweetform.html")


@login_required
def savetweet(request):
    context = {}
    if request.method == "POST":
        tweet = request.POST['tweet']
        user = request.user  # ✅ get the logged-in user
        image = request.FILES.get('photo')  # LEARNING: 1) Text data — like the value from a <textarea> or <input type="text">
        # 2) By using .get(), if no file is uploaded, it won’t throw a MultiValueDictKeyError.
        # → This goes into request.POST
        # File data — like images, PDFs, videos, etc. from <input type="file">
        # → This goes into request.FILES
        # Because files are binary data, not regular key-value strings. They’re uploaded as chunks, not as simple form fields.

        saved = Tweets(user=user, text=tweet, photo=image) # LEARNING: User is required because anonymous tweets are not allowed.
        saved.save()  # LEARNING: Commit=True(by default it's true) means That is saving the data to the database.
        return redirect('index')  # That is sending the data to the html page (index.html) and that is fetching the data from the database.
    return render(request, "index.html")


@login_required
def edit_tweet(request, tweet_id):
    context = {}
    tweet = get_object_or_404(Tweets, id=tweet_id, user=request.user)  # tweet is an instance of your Tweets model:
    # user=request.user; implies that only login user can edit his tweet not any other tweets
    if request.method == 'POST':
        new_text = request.POST.get('tweet')
        new_photo = request.FILES.get('photo')

        tweet.text = new_text  # .text refers to text field defined in model
        if new_photo:
            tweet.photo = new_photo  # .photo refers to photo  field in table/model.
        tweet.save()  # saving to model

        return HttpResponseRedirect('/index/')  # or wherever you want to redirect after editing
    context = {
        'tweet': tweet  # object is passed here as vlaue of the key
    }
    return render(request, 'update_tweet.html', context)


@login_required
def delete_tweet(request, tweet_id):
    context = {}
    tweet = get_object_or_404(Tweets, id=tweet_id, user=request.user)

    if request.method == 'POST':

        tweet.delete()
        return redirect('index')
    context = {
        'tweet': tweet
    }
    return render(request, 'tweet_deletion_confirm.html',context)


def custom_404_view(request, exception): # 'exception' handles all the errors that the user mistyped.
    text = f"Error 404! Page not Found!"
    context = {
        'message': text
    }
    return render(request, "404.html", context, status=404)

def custom_500_view(request):
    error_text = f"Something went wrong on our end. Internal Server error 500."
    context = {
        'message': error_text
    }
    return render(request, "500.html", context, status=500)


def picture(request, pic_id):
    pic = Tweets.objects.get(id=pic_id)
    return render(request, "index.html", {'pic': pic})

