from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    ra = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

class LoginForm(forms.Form):
    ra = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        
    )

class ProdutoForm(forms.Form):
    nome = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    descricao = forms.CharField(max_length=200, required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))
    preco = forms.DecimalField(max_digits=10, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    estoque = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    foto = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))