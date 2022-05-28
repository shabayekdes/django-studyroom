from django.forms import ModelForm

from .models import Message

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # django-crispy-forms
        for field in self.fields:
            new_data = {
                "placeholder": 'Write your message here...',
                # "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        self.fields['body'].widget.attrs.update({'rows': '2'})
