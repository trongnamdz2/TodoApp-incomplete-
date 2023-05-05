from django import forms

from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, error_messages={
        "required": "Please fill in the username field."
    })
    password = forms.CharField(widget=forms.PasswordInput(), max_length=100)


class RegisterForm (forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True, max_length=100)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, max_length=100)

    def clean(self):
        super(RegisterForm, self).clean()

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if len(username) < 3:
            self._errors['username'] = self.error_class(['Username cant be lesser than 3'])
        if len(password) < 6:
            self._errors['password'] = self.error_class(['Password must contain 6 charater or above'])
        if self.cleaned_data.get('confirm_password') != self.cleaned_data.get('password'):
            self._errors['confirm_password'] = self.error_class(['Confirm password must be the same with password'])
        if User.objects.all().filter(username=username):
            self._errors['username'] = self.error_class(['This username been already taken.'])
        try:
            int(password)
            self._errors['password'] = self.error_class(['Password must contain a chararacter'])
        except:
            pass
        return self.cleaned_data



class AddTask(forms.Form):
    taskname = forms.CharField(widget=forms.Textarea(attrs={'class': 'auto-expand'}), required=True, label='Quick add Task')

        

class EditForm(forms.Form):
    todo = forms.CharField(max_length=500, required=True)