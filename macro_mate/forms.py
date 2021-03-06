from django import forms
from taggit.forms import TagField

from macro_mate.models import Comment, Meal, MealCategory


class MealForm(forms.ModelForm):
    """The form form handling meal addition / editing. Stars on labels indicate compulsory fields"""

    INGREDIENT_PLACEHOLDER = "Example:\n200g chicken\n50g broccoli\n1tsp olive oil"

    name = forms.CharField(max_length=Meal.NAME_MAX_LENGTH,
                           label="Meal Name:*")

    categories = forms.ModelMultipleChoiceField(label="Categories:*",
                                                queryset=MealCategory.objects,
                                                widget=forms.CheckboxSelectMultiple(),
                                                required=True)

    servings = forms.IntegerField(min_value=1,
                                  initial=1,
                                  label="# Servings:*",
                                  help_text="Nutritional values will be calculated from this.")

    tags = TagField(widget=forms.TextInput(attrs={'placeholder': 'Add tags'}),
                    required=False,
                    label="Add tags:")

    ingredients = forms.CharField(widget=forms.Textarea(attrs={'placeholder': INGREDIENT_PLACEHOLDER}),
                                  required=True,
                                  label="Ingredients:*",
                                  help_text="Each ingredient should be written on a new line. Please include any units, e.g: '20g tomatoes'")

    # This defaults to http://
    # In the future it could be modified to be more generic with regex
    url = forms.URLField(max_length=Meal.URL_MAX_LENGTH,
                         required=False,
                         label="Recipe Link:",
                         help_text="Write your link to an external recipe here.")

    notes = forms.CharField(widget=forms.Textarea,
                            required=False,
                            label="Notes:",
                            help_text="Any additional notes for your meal.")

    # Empty files to use placeholder in templates
    image = forms.ImageField(allow_empty_file=True, required=False)

    # Hidden nutrition fields to be set with javascript following AJAX reply
    # Some initial data provided for ensuring data integrity.
    calories_unit = forms.CharField(
        widget=forms.HiddenInput(), initial=Meal.CALORIE_DEFAULT_UNIT)
    calories_quantity = forms.FloatField(
        widget=forms.HiddenInput(), min_value=0, initial=0)

    fat_unit = forms.CharField(
        widget=forms.HiddenInput(), initial=Meal.FAT_DEFAULT_UNIT)
    fat_quantity = forms.FloatField(
        widget=forms.HiddenInput(), min_value=0)

    protein_unit = forms.CharField(
        widget=forms.HiddenInput(), initial=Meal.PROTEIN_DEFAULT_UNIT)
    protein_quantity = forms.FloatField(
        widget=forms.HiddenInput(), min_value=0)

    carbs_unit = forms.CharField(
        widget=forms.HiddenInput(), initial=Meal.CARBS_DEFAULT_UNIT)
    carbs_quantity = forms.FloatField(
        widget=forms.HiddenInput(), min_value=0)

    class Meta:
        # Associate
        model = Meal
        # Include all fields except owners and creation info
        exclude = ('owner', 'users', 'created_date', 'modified_date')

    # Allow cleaning up by appending http://
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with https (because we secure...), prepend...
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url

        return cleaned_data


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)
