from django.db import models

# New User model
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150, unique=False, null=False, blank=True, default="")
    lastname = models.CharField(max_length=150, unique=False, null=False, blank=True, default="")
    email = models.EmailField(unique=True, null=False, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Link(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(default="")
    icon = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0, null=False, blank=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="links", null=True)


    def __str__(self):
        return self.title