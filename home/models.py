from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
import datetime
from django.core.exceptions import ValidationError

class User( AbstractUser):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    avatar = models.URLField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=255, null=False, unique=True)
    name = models.CharField(max_length=255, null=False, default="")
    address = models.CharField(max_length=255, null=False, default="")
    role = models.IntegerField(default=0) 
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    forget_password_token = models.CharField(max_length=255, blank=True, null=True)
    forget_password_expires_at = models.DateTimeField(blank=True, null=True)
    reset_password_token = models.CharField(max_length=255, blank=True, null=True)
    reset_password_expires_at = models.DateTimeField(blank=True, null=True)
    online_status = models.BooleanField(default=False)

    class Meta:
        db_table = 'user'


class Category(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    sub = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.sub} ({self.category.name if self.category else 'No Category'})"

class Content(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=False)
    image_url = models.URLField(max_length=200, blank=True, null=True)  
    image_file = models.ImageField(upload_to='images/', blank=True, null=True)  
    content = models.TextField()
    author = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)  
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def clean(self):
      
        if self.image_url and self.image_file:
            raise ValidationError("Chỉ được chọn một trong hai: image_url hoặc image_file.")
        if not self.image_url and not self.image_file:
            raise ValidationError("Cần phải chọn ít nhất một trong hai: image_url hoặc image_file.")

class Comment(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    title = models.TextField(default="No title") 
    author = models.CharField(max_length=255, null=True, blank=True)  
    created_date = models.DateTimeField(auto_now_add=True)  
    content = models.ForeignKey(Content, related_name='comments', on_delete=models.CASCADE)  

    def __str__(self):
        return self.content[:50]  

class SoftDeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    
class SoftDeleteMixin(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletedManager()  
    all_objects = models.Manager() 

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, soft=True):
        if soft:
            self.is_deleted = True
            self.deleted_at = datetime.datetime.now()
            self.save()
        else:
            super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

class RefreshToken(SoftDeleteMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="refresh_token")
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = 'refreshtoken'

    def __str__(self):
        return f"RefreshToken for {self.user.username}"