from django.shortcuts import render, redirect, get_object_or_404
from .forms import VideogameForm
from .models import VideoGame
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.

@login_required
@permission_required ('videogames_register.view_videogame', raise_exception=True)
def videogame_list(request):
    context = {'videogame_list': VideoGame.objects.all()}
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
        return redirect('/videogame/list')

@login_required
@permission_required('videogames_register.delete_videogame', raise_exception=True)
def videogame_delete(request,id):
    videogame = VideoGame.objects.get(pk=id)
    videogame.delete()
    return redirect('/videogame/list')


