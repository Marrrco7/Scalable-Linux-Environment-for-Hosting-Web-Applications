from django.db.models import Q, Count
from django.db.models.functions import ExtractYear
from django.shortcuts import render, redirect, get_object_or_404
from .forms import VideogameForm, DeveloperForm, ReviewForm, UserProfileForm, CopyForm
from .models import VideoGame, Developer, Review, UserProfile, Copy
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db import connection



@login_required
@permission_required ('videogames_register.view_videogame', raise_exception=True)
def videogame_list(request):
    query = request.GET.get("query")
    videogames = VideoGame.objects.all()

    if query:
        videogames = videogames.filter(
            Q(title__icontains=query) |
            Q(genre__title__icontains=query)
        )


    context = {'videogame_list': videogames, 'query': query}
    return render(request, "videogames_register/videogame_list.html", context)

@login_required
@permission_required('videogames_register.add_videogame', raise_exception=True)
def videogame_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = VideogameForm()
        else:
            videogame = VideoGame.objects.get(pk=id)
            form = VideogameForm(instance=videogame)
        return render(request, "videogames_register/videogame_form.html", {'form': form})
    else:
        if id == 0:
            form = VideogameForm(request.POST)
        else:
            videogame = VideoGame.objects.get(pk=id)
            form = VideogameForm(request.POST,instance= videogame)
        if form.is_valid():
            form.save()
        return redirect('videogame_list')

@login_required
@permission_required('videogames_register.delete_videogame', raise_exception=True)
def videogame_delete(request,id):
    videogame = VideoGame.objects.get(pk=id)
    videogame.delete()
    return redirect('videogame_list')


def developer_list(request):
    developers = Developer.objects.all()
    return render(request, "videogames_register/developer_list.html", {"developers": developers})

def developer_form(request):
    if request.method == "POST":
        form = DeveloperForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('developer_list')
    else:
        form = DeveloperForm()
    return render(request, "videogames_register/developer_form.html", {"form": form})


def review_list(request):
    reviews = Review.objects.all()
    return render(request, "videogames_register/review_list.html", {"reviews": reviews})

def review_form(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = ReviewForm()
    return render(request, "videogames_register/review_form.html", {"form": form})


def userprofile_list(request):
    profiles = UserProfile.objects.all()
    return render(request, "videogames_register/userprofile_list.html", {"profiles": profiles})

def userprofile_form(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('userprofile_list')
    else:
        form = UserProfileForm()
    return render(request, "videogames_register/userprofile_form.html", {"form": form})


def copy_list(request):
    copies = Copy.objects.all()
    return render(request, "videogames_register/copy_list.html", {"copies": copies})

def copy_form(request):
    if request.method == "POST":
        form = CopyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('copy_list')
    else:
        form = CopyForm()
    return render(request, "videogames_register/copy_form.html", {"form": form})



#REPORTING


def report_top_genres(request):
    data = (
        VideoGame.objects
        .values('genre__title')
        .annotate(game_count = Count('id'))
        .order_by('-game_count')[:5]
    )

    return render(request, "videogames_register/report_top_genres.html", {'data':data})


def report_releases_over_time(request):
    data = (
        VideoGame.objects
        .annotate(year=ExtractYear('release_date'))
        .values('year')
        .annotate(release_count=Count('id'))
        .order_by('year')
    )
    return render(request, "videogames_register/report_releases_over_time.html", {
        'data': data
    })


def report_cumulative_releases(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT year, games_this_year, cumulative_total 
            FROM analytics.cumulative_releases 
            ORDER BY year;  
        """)
        rows = cursor.fetchall()

    data = [
        {"year": row[0], "games_this_year": row[1], "cumulative_total": row[2]}
        for row in rows
    ]
    return render(request, "videogames_register/report_cumulative_releases.html", {
        "data": data
    })


from django.shortcuts import render

def report_dashboard(request):
    return render(request, "videogames_register/report_dashboard.html")
