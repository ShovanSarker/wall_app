from django.db import models
from wall.models import BaseModel
from wall.models import Writer


class Post(BaseModel):

    writer = models.ForeignKey(Writer, related_name='user_post_owner', on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    content = models.CharField(max_length=2048, null=False)
    published = models.BooleanField(default=True)

    class Meta:
        app_label = "wall"
        db_table = "post"


class Comment(BaseModel):
    post = models.ForeignKey(Post, related_name='post_comment', on_delete=models.CASCADE)
    commenter = models.ForeignKey(Writer, related_name='user_commenter_on_post', on_delete=models.CASCADE)
    content = models.CharField(max_length=1024, null=False)
    published = models.BooleanField(default=True)

    class Meta:
        app_label = "wall"
        db_table = "comment"
