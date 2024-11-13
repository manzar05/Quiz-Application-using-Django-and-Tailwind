from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self,username,password=None):
        if not username:
            raise ValueError("Username Required")
        user = self.model(username=username)
        user.set_password(password)   
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,password=None):
        user = self.create_user(username=username,password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser):
    username= models.CharField(max_length=50,unique=True)
    email= models.CharField(max_length=50,null=True)
    first_name= models.CharField(max_length=20,null=True)
    last_name= models.CharField(max_length=20,null=True)
    is_admin = models.BooleanField(default=0)
    is_active= models.BooleanField(default=0)

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    @property
    def is_staff(self):
        return self.is_admin
    

class Questions(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.CharField(max_length=255, null=True, blank=True)
    option1 = models.CharField(max_length=255, null=True, blank=True)
    option2 = models.CharField(max_length=255, null=True, blank=True)
    option3 = models.CharField(max_length=255, null=True, blank=True)
    option4 = models.CharField(max_length=255, null=True, blank=True)
    correct_answer = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['question']),           # Index on question for faster lookups
            models.Index(fields=['correct_answer']),     # Index on correct_answer if queried frequently
        ]

# class TestSet(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     testset_name = models.CharField(max_length=255, null=True, blank=True)
#     user = models.ForeignKey(User,on_delete=models.CASCADE ,related_name="testset_user", to_field="id", db_column="user")
#     created_date = models.DateTimeField(null=True)
#     total_marks = models.IntegerField(default=20)

#     class Meta:
#         indexes = [
#             models.Index(fields=['testset_name']),       # Index on testset_name for fast searches
#             models.Index(fields=['user']),               # Index on user to speed up user lookups
#             models.Index(fields=['created_date']),       # Index on created_date for faster ordering or filtering
#         ]

class UserResponse(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_response = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE ,related_name="user_response_user", to_field="id", db_column="user")
    question = models.ManyToManyField(Questions, related_name="user_response_question", db_column="question")
    marks = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False) 
    class Meta:
        indexes = [
            models.Index(fields=['user_response']),      # Index on user_response for faster querying
            models.Index(fields=['user']),           # Index on test_set for efficient joining/filtering
        ]
