from django import forms
from .models import VideoGame


class VideogameForm(forms.ModelForm):

    class Meta:
        model = VideoGame
        fields = ('title','release_date','description','genre')
        labels = {
            'title':'Title',
            'release_date':'Release Date',
        }

    def __init__(self, *args, **kwargs):
        super(VideogameForm,self).__init__(*args, **kwargs)
        self.fields['genre'].empty_label = "Select"
        self.fields['description'].required = False