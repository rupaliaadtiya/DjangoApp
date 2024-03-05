from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phonenumber, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phonenumber=phonenumber,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phonenumber, password=None, **extra_fields):
        user = self.create_user(
            email,
            first_name,
            last_name,
            phonenumber,
            password,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email",max_length=255,unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phonenumber = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "user"

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phonenumber']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "user_role"
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.name

    
class Permission(models.Model):
    name = models.CharField(max_length=255, unique=True)
    content_type = models.ForeignKey(
        'contenttypes.ContentType', on_delete=models.CASCADE, related_name='account_permissions'
    )
    codename = models.CharField(max_length=100)

    class Meta:
        db_table = "user_permission"
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"

    def __str__(self):
        return self.name + " (" + str(self.content_type) + ")"
    
    
class RolePermission(models.Model):
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    permission = models.ForeignKey('Permission', on_delete=models.CASCADE)

    class Meta:
        db_table = "user_role_permissions"
        unique_together = ('role', 'permission')  # Ensure unique combination of role and permission

    def __str__(self):
        return f"{self.role} - {self.permission}"
