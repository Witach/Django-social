from django.db import models

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message.html = model.TextField(editable=False)
    group = models.ForeignKey(Group, null=True,blank=True)

    def __str__(self):
        return self.message

    def save(self, *args,**kwargs):
        self.message_html = self.message
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("posts:single",kwargs = {"username":self.user.username,"pk":self.pk})

    class Meta():
        ordering = ["-created_at"]
        unique_together = ["user","message"]
