from django.forms import ModelForm
from zr.models import PostSubscription


class PostSubscriptionForm(ModelForm):
    class Meta:
        model = PostSubscription