from django.db import models
from accounts.models import UserAccount
from django.db.models import Avg
from cloudinary.models import CloudinaryField
# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    project_link = models.URLField(max_length=200)
    image = CloudinaryField("image")
    liked = models.ManyToManyField(UserAccount, null=True, blank=True, related_name='liked')
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def num_likes(self):
        return self.liked.all().count()

    def average_review(self):
        reviews = RatingReview.objects.filter(project = self, status=True).aggregate(average = Avg('rating'))
        avg = 0

        if reviews['average'] is not None:
            avg = float(reviews['average'])
        
        return avg

    def __str__(self):
        return self.name

LIKED_CHOICES = (
    ('like', 'like'),
    ('unlike', 'unlike')
)

class Like(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    value = models.CharField(choices=LIKED_CHOICES, default='like' ,max_length=10)

    def __str__(self):
        return str(self.post)

class RatingReview(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name = 'reviews')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='users')
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500)
    rating = models.FloatField(blank=True)
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username