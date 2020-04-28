from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from PIL import Image


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('User must have an email address')

        if not full_name:
            raise ValueError('User must have a full_name')

        if not password:
            raise ValueError('User must have a password')
        user = self.model(email=self.normalize_email(email), full_name=full_name)
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.save()
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(email=email, password=password, is_staff=True)
        return user

    def create_superuser(self, email, full_name, password):
        user = self.create_user(email=email, full_name=full_name, password=password, is_staff=True, is_admin=True)
        return user


class User(AbstractBaseUser):
    # class Meta:
    #     db_table = 'user'

    POSITION = [
        ('commission', 'Commission'),
        ('secretary', 'Secretary'),
        ('hr', 'HR')
    ]

    email = models.EmailField(unique=True, max_length=255)
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=25, choices=POSITION)
    image = models.ImageField(default='employee_pics/default.jpg', upload_to='employee_pics')
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def get_full_name(self):
        return self.full_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    @property
    def is_secretary(self):
        if self.position == 'secretary':
            return True
        else:
            return False

    @property
    def is_commission(self):
        if self.position == 'commission':
            return True
        else:
            return False

    @property
    def is_hr(self):
        if self.position == 'hr':
            return True
        else:
            return False
