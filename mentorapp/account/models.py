# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_mentor', False)
        extra_fields.setdefault('is_mentee', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_mentor', False)
        extra_fields.setdefault('is_mentee', False)

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    username = None
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=100, default=False)
    last_name = models.CharField(max_length=100, default=False)
    is_mentor = models.BooleanField('student status', default=False)
    is_mentee = models.BooleanField('teacher status', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()



class Mentee(models.Model):
    """Mentee models"""

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)

    # interests = models.OneToOneField(Subject, related_name='mentees', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class Mentor(models.Model):
    """Mentor models"""

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)

    # interests = models.OneToOneField(Subject, related_name='mentors', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class Msg(models.Model):
    """Message Model"""

    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE, null=True)
    receipient = models.ForeignKey(User, related_name="receipient", on_delete=models.CASCADE)
    msg_content = models.TextField(max_length=1000)
    sent_at = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(blank=True, null=True)


    def __str__(self):
        return "From {}, to {}".format(self.sender.email, self.receipient.email)

    def save(self, *args, **kwargs):
        if not self.id:
            self.sent_at = timezone.now()

        super(Msg, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-sent_at']