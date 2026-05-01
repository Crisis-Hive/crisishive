from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/',blank=True,null=True)
    bio= models.TextField(blank=True)
    phone = models.CharField(max_length=20,blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - Profile"