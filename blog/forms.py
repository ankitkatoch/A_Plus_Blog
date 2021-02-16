from django import forms
from tinymce import TinyMCE
from .models import BlogModel


class TinyMCEWidget(TinyMCE):
	def use_required_attribute(self, *args):
		return False


class PostForm(forms.ModelForm):
	description = forms.CharField(
		widget=TinyMCEWidget(
			attrs={'required': False, 'cols': 30, 'rows': 30}
		)
	)

	class Meta:
		model = BlogModel
		fields = '__all__'
