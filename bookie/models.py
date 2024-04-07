from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models import OneToOneField

from django.utils.translation import gettext_lazy as _


class CustomBookieManager(BaseUserManager):
    def create_user(self, email, age, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Please enter your email address!'))
        if not age:
            raise ValueError(_("Please enter your age."))

        email = self.normalize_email(email)
        user = self.model(email=email, age=age, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, age, password=None, **extra_fields):

        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self.create_user(email, age, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)


class Bookie(AbstractBaseUser, PermissionsMixin):

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    MAX_EMAIL_LENGTH = 120
    DEFAULT_AGE = 18

    email = models.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
    )
    age = models.PositiveIntegerField(
        default=DEFAULT_AGE,
        help_text="This field is important for our site."
    )

    date_joined = models.DateTimeField(
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['age']

    objects = CustomBookieManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class BookieProfile(models.Model):

    MAX_COUNTRY_LENGTH = 50
    MAX_BIO_LENGTH = 300

    user = OneToOneField(
        Bookie,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    country = models.CharField(
        max_length=MAX_COUNTRY_LENGTH,
        null=True,
        blank=True,
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures',
        default='no_profile.png'
    )

    bio = models.TextField(
        max_length=MAX_BIO_LENGTH,
        help_text="Share something about yourself.",
        null=True,
        blank=True
    )

    want_to_read = models.ManyToManyField(
        'book.Book',
        blank=True,
        default=None,
        related_name='want_to_read',
    )

    have_read = models.ManyToManyField(
        'book.Book',
        blank=True,
        default=None,
        related_name="have_read"
    )


    def get_bookie_name(self):
        return self.user.email.split("@")[0].capitalize()

    def get_profile_caption(self):
        return f"{self.get_bookie_name()}`s Profile"


class GetUsersByDateJoined(SimpleListFilter):

    title = "Date Joined"
    parameter_name = 'date_joined'

    def lookups(self, request, model_admin):
        return (
            ('new_users', "New users"),
            ('old_users', 'Old users')
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        elif self.value() == "new_users":
            return queryset.order_by("-date_joined")
        elif self.value() == "old_users":
            return queryset.order_by("date_joined")


class UserAdmin(admin.ModelAdmin):
    list_display = ('date_joined', 'email',)
    list_filter = (GetUsersByDateJoined, )
    search_fields = ('email', )
