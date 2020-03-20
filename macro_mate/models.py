from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from taggit.managers import TaggableManager
from multiselectfield import MultiSelectField

from django.template.defaultfilters import slugify


class UserProfile(models.Model):
    """A user profile model linked to Django's base User. Application specific fields are added."""

    # Link to the basic User account
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Set name to the user's name
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a corresponding UserProfile object when a User is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the userprofile accordingly when modifications to a user are made"""
    instance.userprofile.save()


# THIS MUST BE POPULATED WHEN DEPLOYING APP
class MealCategory(models.Model):
    """A model for holding a required category for a meal, e.g. breakfast.
    This must be pre-populated prior to deployment."""

    CATEGORY_MAX_LENGTH = 12

    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    SNACK = "Snack"

    MEAL_CATEGORIES = [BREAKFAST, LUNCH, DINNER, SNACK]

    category = models.CharField(max_length=CATEGORY_MAX_LENGTH,
                                unique=True)

    slug = models.SlugField()

    # Override save to create a slug automatically
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category)
        super(MealCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.category


class Meal(models.Model):

    """A model for a meal."""

    NAME_MAX_LENGTH = 128
    URL_MAX_LENGTH = 255
    UNIT_MAX_LENGTH = 12

    CALORIE_DEFAULT_UNIT = 'kcal'
    FAT_DEFAULT_UNIT = 'g'
    PROTEIN_DEFAULT_UNIT = 'g'
    CARBS_DEFAULT_UNIT = 'g'

    # Reference Fields
    # ----------------

    # Date and time created / modified
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # The owning user
    # on_delete: When the user is deleted, all their meals are deleted
    owner = models.ForeignKey(UserProfile,
                              on_delete=models.CASCADE,
                              related_name='%(class)s_owner')

    # Users
    # Each user can have many meals in their DB, which aren't necessarily owned by them
    users = models.ManyToManyField(UserProfile,
                                   related_name='%(class)s_users')

    name = models.CharField(max_length=NAME_MAX_LENGTH)

    # This needs to be enforced to have MIN: 1 in the forms field
    categories = models.ManyToManyField(MealCategory)

    # Uses Django Taggit's TaggableManager, which can add tags.
    # https://django-taggit.readthedocs.io/en/latest/
    tags = TaggableManager(blank=True)

    servings = models.IntegerField(default=1)

    # Ingredient field
    # ----------------
    # Should be a comma / new line seperated list.
    # The API call will throw errors to the user and should disallow analysis if these
    # cannot be parsed correctly.
    ingredients = models.TextField(blank=True)

    url = models.URLField(max_length=URL_MAX_LENGTH, blank=True)

    notes = models.TextField(blank=True)

    # Nutrition Fields
    # ----------------
    # These values are cached from the API, should NOT be visible to user in a form

    calories_quantity = models.FloatField(default=0.0)
    calories_unit = models.CharField(max_length=UNIT_MAX_LENGTH,
                                     default='kcal')

    fat_quantity = models.FloatField(default=0.0)
    fat_unit = models.CharField(max_length=UNIT_MAX_LENGTH,
                                default='g')

    protein_quantity = models.FloatField(default=0.0)
    protein_unit = models.CharField(max_length=UNIT_MAX_LENGTH,
                                    default='g')

    carbs_quantity = models.FloatField(default=0.0)
    carbs_unit = models.CharField(max_length=UNIT_MAX_LENGTH,
                                  default='g')

    image = models.ImageField(upload_to='meal_images',
                              blank=True)

    def __str__(self): return self.name


class Comment(models.Model):
    """A class for comments on models"""

    # Associate many comments to a meal
    meal = models.ForeignKey(
        Meal, on_delete=models.CASCADE, related_name='comments')

    # Associate many comments to a user
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    body = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.owner)
