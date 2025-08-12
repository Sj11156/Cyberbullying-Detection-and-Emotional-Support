from django import forms
from django.forms import CharField
from socialapp.models import pmodel,smodel

# ----------------------------------------------user registration---------------------------------------------------------------------------------			 
class pform(forms.Form):
	pos = forms.CharField(max_length=100)
	post_image = forms.FileField()
	class Meta:
		model = pmodel
		fields = ['pos','userid','nme','date','post_image']
		
# ------------------------
class sform(forms.Form):
	uid = forms.CharField(max_length=100)
	p_image = forms.FileField()
	class Meta:
		model = smodel
		fields = ['uid','p_image']