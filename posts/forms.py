from django import forms
from posts.models import Post
from groups.models import Group
class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ("message","group")

    def __init__(self,*args,**kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args,**kwargs)
        if user is not None:
            self.fields["group"].queryset = (Group.objects.filter(pk__in=user.groups.value_list("group__pk")))
