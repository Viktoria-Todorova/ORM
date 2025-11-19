from django import forms
from fruitipediaApp.fruits.models import Fruit,Category

class CategoryBaseForm(forms.ModelForm): #it's django form
    class Meta:
        model = Category #all the fields that our category has
        fields = '__all__'

class CategoryForm(CategoryBaseForm):
    pass

class FruitBaseForm(forms.ModelForm):
    class Meta:
        model = Fruit
        fields = '__all__'

class FruitAddForm(FruitBaseForm):
    pass


class EditFruitForm(FruitBaseForm):
    pass

class FruitDeleteForm(FruitBaseForm):
    pass