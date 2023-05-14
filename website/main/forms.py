from django import forms
from django.forms import ModelForm
from .models import List

class ListForm(ModelForm):
    class Meta:
        model = List
        fields = ('id', 'DateTime', 'Car', 'Detail', 'Location')
        labels = {
            'DateTime':'時間 YYYY-MM-DD HH:MM:SS',
            'Car':'車輛',  
            'Detail':'案件細項', 
            'Location':'發生地點', 
        }
        widgets = {
            'DateTime': forms.TextInput(attrs={'class':'form-control', 'placeholder':'time'}),
            'Car': forms.TextInput(attrs={'class':'form-control', 'placeholder':'car'}),
            'Detail': forms.TextInput(attrs={'class':'form-control', 'placeholder':'detail'}),
            'Location': forms.TextInput(attrs={'class':'form-control', 'placeholder':'location'})
        }