from django.db import models
from django.conf import settings


class CommentQueryset(models.QuerySet):

    def posted_on(self, pulso):
        return self.filter(pulso=pulso)

    def created_by(self, author):
        return self.filter(author=author)


class Comment(models.Model):
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pulso = models.ForeignKey(
        to='pulsos.Pulso',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.CharField(max_length=145)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CommentQueryset.as_manager()

    class Meta:
        ordering = ['-created_at']
