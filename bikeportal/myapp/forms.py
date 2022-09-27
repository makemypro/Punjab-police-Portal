from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

city_choice = (('lahore','lahore'), ('Karachi','Karachi'),('Faislbad', 'Faislbad'))

class Registration(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        def __str__(self):
            return self.email

# class CheckoutForm(forms.ModelForm):
#     first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'fblock', 'placeholder': 'First Name'}))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'fblock' , 'placeholder': 'Last Name'}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'fblock', 'placeholder': 'example@gmail.com'}),error_messages={'required':'*'})
#     phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'fblock', 'placeholder':'mobile number'}))
#     zip_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'fblock', 'placeholder': 'Zip Code/Area Code'}))
#     address = forms.CharField(widget=forms.TextInput(attrs={'class': 'fblock', 'placeholder': 'Mention Your Address'}))
#     city = forms.CharField(widget=forms.Select(attrs={'class': 'fblock'}, choices=city_choice))
#     delivery_instruction = forms.CharField(widget=forms.TextInput(attrs={'class': 'fblock', 'placeholder': 'Mention Ddelivery Instructions'}))
    
    
    
#     # def __init__(self, *args, **kwargs):
#     #     user = kwargs.pop('user','')
#     #     super(EngComplain, self).__init__(*args, **kwargs)
#     #     self.fields['user']=forms.ModelChoiceField(queryset=User.objects.filter(user=user))
    
#     def clean(self):
#         cleaned_data = super().clean()
#         first_name = self.cleaned_data['first_name']
#         last_name = self.cleaned_data['last_name']
#         email = self.cleaned_data['email']
#         phone_number = self.cleaned_data['phone_number']
#         if type(first_name) == int:
#             raise forms.ValidationError('Name should be in character form')
#         if first_name.isalnum()==False:
#             raise forms.ValidationError('integer or alphnumeric characters not allow')
#         if '@' not in email:
#             raise forms.ValidationError('Invalid mail address')
#         if len(phone_number) < 11:
#             raise forms.ValidationError('Phone number not exist')
        
#     class Meta:
#         model = delivery_address
#         fields = [
#             'first_name', 'last_name', 'email','phone_number', 'zip_code',  'address', 'city','delivery_instruction',]
