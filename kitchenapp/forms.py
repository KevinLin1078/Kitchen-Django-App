from django import forms 
from .models import  User, Menu, Kitchen, KitchenImage, Kitchen


# kitchen = forms.mode(widget = forms.HiddenInput(), required = False)
class SignUpForm(forms.ModelForm):   
   question_1 = forms.CharField(max_length=100, required = True, initial="What is your favorite color?")
   answer_1 = forms.CharField(required = True)
   question_2 = forms.CharField(max_length=100, required = True, initial="What is your favorite place to live?")
   answer_2 = forms.CharField(required = True)
   class Meta:
      model = User
      fields = "__all__"
      labels = {
        "is_provider": "Become a seller"
      }

   def __init__(self, *args, **kwargs):
      super(SignUpForm, self).__init__(*args, **kwargs) 
      fields = self.fields
      fields['question_1'].widget.attrs['style'] = 'width:250px;'
      fields['question_2'].widget.attrs['style'] = 'width:300px;'
      fields['question_1'].widget.attrs['class'] = "w3-bar-item w3-button"
      fields['question_2'].widget.attrs['class'] = "w3-bar-item w3-button"
      fields['question_1'].widget.attrs['readonly'] = True
      fields['question_2'].widget.attrs['readonly'] = True
      fields['is_provider'].required = False


class LoginForm(forms.Form):
   username  = forms.CharField(max_length=100, required = True)
   password = forms.CharField(max_length=32, widget=forms.PasswordInput, required=True)
   
   

class AddDishForm(forms.Form):
   dish_name = forms.CharField(max_length=50, required=True)
   price =  forms.DecimalField(max_digits=10, decimal_places=2, required=True)
   is_vegan = forms.BooleanField(required=False)



class AddKitchenForm(forms.Form):
   kitchen_name = forms.CharField(max_length=50, required=True)
   image = forms.ImageField(required=True)

'''
class AddDishForm(forms.ModelForm):
   
   class Meta:
      model = Menu
      fields = "__all__"

   class KitchenChoiceField(forms.ModelChoiceField):
      def label_from_instance(self, obj):
         return obj.kitchen_name

   def __init__(self, *args, **kwargs):
      super(AddDishForm, self).__init__(*args, **kwargs)
      fields = self.fields
      fields['kitchen']=forms.ModelChoiceField(queryset=Kitchen.objects.all(), required=True, initial=0)
      fields['kitchen'].widget.attrs['style'] = 'width:100px;'
      fields['kitchen'].label_from_instance = lambda obj: "%s" % obj.kitchen_name
      fields['is_vegan'].required=False
'''