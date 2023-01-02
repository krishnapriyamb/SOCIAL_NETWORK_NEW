from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models import Count


class Posts(models.Model):
    image=models.ImageField(upload_to="image",null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    create_date=models.DateField(auto_now_add=True)
    like=models.ManyToManyField(User,related_name="upvotes")

    @property
    def fetch_comments(self):
        comments=self.comments_set.all().annotate(up_count=Count('like')).order_by('-like')
        return comments

    def __str__(self):
        return self.title

class Comments(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment=models.CharField(max_length=100)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

