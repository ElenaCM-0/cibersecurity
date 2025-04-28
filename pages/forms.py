from django.forms import ModelForm
from .models import minipage

# Create the form class.
class minipageForm(ModelForm):
     def __init__(self, *args, user, **kwargs):
        super(minipageForm, self).__init__(*args, **kwargs)
        self.user = user
        
     def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.owner = self.user
        if commit:
            instance.save()
        return instance


     class Meta:
         model = minipage
         fields = ['name', 'content']
         error_messages = {
             'name' : {
                 'unique': "The page's name must be unique and this one is already taken!"
             }
         }