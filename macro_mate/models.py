from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from taggit.managers import TaggableManager
from multiselectfield import MultiSelectField


class UserProfile(models.Model):
    """A user profile model linked to Django's base User class."""

    # User
    # ----
    # Link to the basic User account
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add user profile picture
    profilePicture = models.ImageField(
        upload_to='profile_pictures', blank=True)

    # Set profile name to the user name
    def __str__(self):
        return self.user.username

# The following receivers synchronise User_Profile with User when a
# new user is created or saved.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


# TODO: Create rating functionality for meal
# TODO: Create comment class for meal

# THIS MUST BE POPULATED WHEN DEPLOYING APP
class MealCategory(models.Model):
    """A model for holding a required category for a meal, e.g. breakfast"""
    # Meal Category Choices
    # ---------------------
    # Uses MultiSelectField. Constants used to programatically create in populate script

    CATEGORY_MAX_LENGTH = 12

    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    SNACK = "Snack"

    MEAL_CATEGORIES = [BREAKFAST, LUNCH, DINNER, SNACK]

    category = models.CharField(max_length=CATEGORY_MAX_LENGTH,
                                unique=True)

    def __str__(self):
        return self.category


class Meal(models.Model):
    """A model for a meal."""

    # Constraints
    # -----------

    NAME_MAX_LENGTH = 128
    URL_MAX_LENGTH = 255
    UNIT_MAX_LENGTH = 12

    CALORIE_DEFAULT_UNIT = 'kcal'
    FAT_DEFAULT_UNIT = 'g'
    PROTEIN_DEFAULT_UNIT = 'g'
    CARBS_DEFAULT_UNIT = 'g'

    # Reference Fields
    # ----------------

    # The owning user
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    # Fields
    # ------

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    url = models.URLField(max_length=URL_MAX_LENGTH, blank=True)

    # Categories
    # ----------
    # This needs to be enforced to have MIN: 1 in the forms field
    categories = models.ManyToManyField(MealCategory)

    # Tags
    # ----
    # Uses TaggableManager, which can add tags.
    tags = TaggableManager(blank=True)

    servings = models.IntegerField(default=1)

    # Ingredient field
    # ----------------
    # Should be a comma / new line seperated list. Enforce at form level.
    # May want to migrate this to another object, but currently not much need as API does heavy lifting.
    ingredients = models.TextField(blank=True)

    notes = models.TextField(blank=True)

    # Nutrition Fields
    # ----------------
    # These values are cached from the API, should NOT be visible to user

    calories_unit = models.CharField(
        max_length=UNIT_MAX_LENGTH, default='kcal')
    calories_quantity = models.FloatField(default=0.0)

    fat_unit = models.CharField(max_length=UNIT_MAX_LENGTH, default='g')
    fat_quantity = models.FloatField(default=0.0)

    protein_unit = models.CharField(max_length=UNIT_MAX_LENGTH, default='g')
    protein_quantity = models.FloatField(default=0.0)

    carbs_unit = models.CharField(max_length=UNIT_MAX_LENGTH, default='g')
    carbs_quantity = models.FloatField(default=0.0)

    image = models.ImageField(blank=True)

    def __str__(self): return self.name
