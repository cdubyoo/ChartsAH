from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Profile, Comment

# changing the form to include email and bio
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

MAX_LENGTH = 250

# create post form
class PostForm(forms.ModelForm):
    class Meta: # declare the form
        model = Post
        fields = ['content']
# make sure form follows rules
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_LENGTH:
            raise forms.ValidationError("Post exceeded max length of 250 characters.")
        return content

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        
