from django import forms
from django.contrib.auth.models import User
from macro_mate.models import UserProfile, Meal
from multiselectfield import MultiSelectFormField
from taggit.forms import *


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profilePicture',)


class MealForm(forms.ModelForm):
    name = forms.CharField(max_length=Meal.NAME_MAX_LENGTH,
                           help_text="Please enter the meal name")
    url = forms.URLField(max_length=Meal.URL_MAX_LENGTH,
                         help_text="Please enter the URL of the meal's recipe.")

    servings = forms.IntegerField(min_value=0,
                                  help_text="Please enter servings")

    # Create an ID for javascript with 'TAGS'
    tags = TagField()

    # Hidden nutrition fields to be set with javascript following AJAX reply
    # Some initial data provided for 'sanitising'
    calorie_unit = forms.CharField(
        widget=forms.HiddenInput(), initial=Meal.CALORIE_DEFAULT_UNIT)
    calorie_quantity = forms.FloatField(
        widget=forms.HiddenInput(), min_value=0, initial=0)

    fat_unit = forms.CharField(
        widget=forms.HiddenInput(), initial=Meal.FAT_DEFAULT_UNIT)
    fat_quantity = forms.FloatField(
        widget=forms.HiddenInput(), min_value=0, initial=0)

    protein_unit = forms.CharField(
        widget=forms.HiddenInput(), initial=Meal.PROTEIN_DEFAULT_UNIT)
    protein_quantity = forms.FloatField(
        widget=forms.HiddenInput(), min_value=0, initial=0)

    carbs_unit = forms.CharField(
        widget=forms.HiddenInput(), initial=Meal.CARBS_DEFAULT_UNIT)
    carbs_quantity = forms.FloatField(
        widget=forms.HiddenInput(), min_value=0, initial=0)

    # It can go wrong here...
    # This is always added
    # caregories = MultiSelectFormField()

    class Meta:
        # Associate
        model = Meal
        # Include all fields except...
        # Hide the foreign key to owner
        exclude = ('owner',)

    # Allow cleaning up by appending http://
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with http, prepend...
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url

        return cleaned_data
