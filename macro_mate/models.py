from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from taggit.managers import TaggableManager
from multiselectfield import MultiSelectField


class User_Profile(models.Model):
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
        User_Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_profile.save()


# TODO: Create rating functionality for meal
# TODO: Create comment class for meal


class Meal(models.Model):
    """A model for a meal."""

    # Constraints
    # -----------

    NAME_MAX_LENGTH = 128
    URL_MAX_LENGTH = 255
    UNIT_MAX_LENGTH = 12

    # Meal Category Choices
    # ---------------------
    # Uses MultiSelectField. Constants used to programatically create in populate script

    BREAKFAST = 1
    LUNCH = 2
    DINNER = 3
    SNACK = 4

    MEAL_CATEGORIES = ((BREAKFAST, 'Breakfast'),
                       (LUNCH, 'Lunch'),
                       (DINNER, 'Dinner'),
                       (SNACK, 'Snack'))

    # Reference Fields
    # ----------------

    # The owning user
    owner = models.ForeignKey(User_Profile, on_delete=models.CASCADE)

    # Fields
    # ------

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    url = models.URLField(max_length=URL_MAX_LENGTH, blank=True)

    # Categories
    # ----------
    # Uses MultiSelectField, which stores a comma separated file in database.
    categories = MultiSelectField(choices=MEAL_CATEGORIES,
                                  min_choices=1,
                                  default=BREAKFAST)

    # Tags
    # ----
    # Uses TaggableManager, which can add tags.
    tags = TaggableManager()

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

    calorie_unit = models.CharField(max_length=UNIT_MAX_LENGTH, default='kcal')
    calorie_quantity = models.FloatField(default=0.0)

    fat_unit = models.CharField(max_length=UNIT_MAX_LENGTH, default='g')
    fat_quantity = models.FloatField(default=0.0)

    protein_unit = models.CharField(max_length=UNIT_MAX_LENGTH, default='g')
    protein_quantity = models.FloatField(default=0.0)

    carbs_unit = models.CharField(max_length=UNIT_MAX_LENGTH, default='g')
    carbs_quantity = models.FloatField(default=0.0)

    def __str__(self): return self.name
