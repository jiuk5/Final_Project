from django import forms
from . models import Profile

class LandmarkForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['imgfile']
        labels = {
            'imgfile': '이미지'
        }