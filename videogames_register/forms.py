from django import forms
from .models import VideoGame, Developer, Review, UserProfile, Copy


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

class DeveloperForm(forms.ModelForm):
    class Meta:
        model = Developer
        fields = ['name', 'founded_year']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user', 'game', 'rating', 'comment']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'country', 'age']

class CopyForm(forms.ModelForm):
    class Meta:
        model = Copy
        fields = ['game', 'serial_number', 'condition']