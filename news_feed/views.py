from django.shortcuts import render, redirect
from feedparser import parse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib import messages


def welcome(request):
    if request.user.is_authenticated:
        return redirect("news_feed")
        # return redirect("news_feed", user_id=request.user.id)
    
    context = {}
    return render(request, 'news_feed/welcome.html', context)


def user_login(request):
    if request.user.is_authenticated:
        return redirect("news_feed")

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist!")
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("news_feed")
            else:
                messages.error(request, "Verify your password please!")

    form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'news_feed/forms.html', context)



@login_required(login_url='user_login')
def user_logout(request):
    logout(request)
    return redirect("user_login")
        

def user_register(request):
    if request.user.is_authenticated:
        return redirect("feed", id=request.user.id)
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("news_feed")
        else:
            if 'email' in form.errors:
                messages.error(request, 'Invalid email address.')
            if 'username' in form.errors:
                messages.error(request, 'Username is already taken.')
            if 'password1' in form.errors:
                messages.error(request, 'Invalid password.')
            if 'password2' in form.errors:
                messages.error(request, 'Confirmation password does not match.')
            return redirect("user_login")

    context = {
        'page': 'Register',
    }
    return render(request, 'news_feed/forms.html', context)


@login_required
def news_feed(request):
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        print("User does not exist!")
    else:
        # Check if the user has a category called 'No Category'
        no_category, created = SourceCategory.objects.get_or_create(
            title='No Category',
            user=user
        )

        # Fetch user categories excluding 'No Category'
        user_categories = SourceCategory.objects.filter(user=user).exclude(title='No Category')

        # Add 'No Category' to the list of user categories
        user_categories = [no_category] + list(user_categories)

        feeds_by_category = []

        for category in user_categories:
            sources = NewsSource.objects.filter(category=category)
            feeds = []

            for source in sources:
                feed = parse(source.url)
                feed_title = feed.feed.title if 'feed' in feed and 'title' in feed.feed else source.url

                if 'entries' in feed and feed.entries:
                    feed_entries = feed.entries
                else:
                    feed_entries = [{'title': "No News", 'published': '', 'description': '', 'link': ''}]

                feeds.append({'source_title': source.title, 'feed_title': feed_title, 'feed_entries': feed_entries})

            feeds_by_category.append({'category': category, 'feeds': feeds})

        # Retrieve NewsSource objects for the current user
        user_sources = NewsSource.objects.filter(category__user=request.user)
        context = {'categories': user_categories, 'feeds_by_category': feeds_by_category, 'user_sources': user_sources}
        return render(request, 'news_feed/news_feed.html', context)


@login_required
def news_sources(request):
    user_categories = SourceCategory.objects.filter(user=request.user)
    user_sources = NewsSource.objects.filter(category__user=request.user)

    context = {'categories': user_categories, 'links': user_sources}
    return render(request, 'news_feed/news_sources.html', context)


@login_required
def add_source(request):
    if request.method == 'POST':
        source_title = request.POST.get('source_title')
        source_link = request.POST.get('source_link')
        source_category_id = request.POST.get('source_category')

        # Check if the current user has the source link already
        existing_source = NewsSource.objects.filter(url=source_link, category__user=request.user).first()

        if existing_source:
            # Handle case where the source link already exists for the user
            print(f"The source link '{source_link}' already exists for the user.")
        else:
            try:
                source_category = SourceCategory.objects.get(id=source_category_id, user=request.user)
            except SourceCategory.DoesNotExist:
                # Handle case where the category does not exist for the user
                print(f"The selected category does not exist for the user.")
                return redirect('news_sources')

            # Create the NewsSource instance with the retrieved category instance
            NewsSource.objects.create(
                title=source_title,
                url=source_link,
                category=source_category
            )
    
    return redirect('news_sources')


@login_required
def delete_source(request, source_id):
    if request.method == 'POST':
        try:
            NewsSource.objects.get(id=source_id).delete()
        except:
            return redirect('news_sources')
            
    return redirect('news_sources')


@login_required
def add_category(request):
    if request.method == 'POST':
        category_title = request.POST.get('category_title').capitalize()

        # Ensure the category with the same title does not exist for the current user
        existing_category = SourceCategory.objects.filter(user=request.user, title=category_title).first()

        if not existing_category:
            # Create a new category for the current user
            new_category = SourceCategory.objects.create(
                title=category_title,
                user=request.user
            )
            print(f"The category '{new_category.title}' has been added for the user.")

    return redirect('news_sources')


@login_required
def delete_category(request):
    if request.method == 'POST':
        try:
            category_id = request.POST.get('category_for_deletion')
            print("category id ::::: ", category_id)
            SourceCategory.objects.get(id=category_id).delete()
        except:
            return redirect('news_sources')

    return redirect('news_sources')



