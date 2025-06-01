from django.db import models


# New User model
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Project(models.Model):
    type = models.CharField(max_length=200)
    image = models.URLField(blank=True, null=True)
    tag = models.JSONField()
    delayAnimation = models.CharField(max_length=50, default="0")
    modalDetails = models.JSONField(default=list)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects", null=True)


    def __str__(self):
        return self.modalDetails.project
