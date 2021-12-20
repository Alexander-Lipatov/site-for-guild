from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.forms import TextInput

from users.models import User


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('game_nick', 'tel',)  # 'full_name',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format

        user = super(UserAdminCreationForm, self).save(commit=False)
        # user.tel = user.zipCode.zip_country + user.tel
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(help_text=("Если пользователь забыл свой пароль от аккаунта, то его можно "
                                                    "сменить по нажатию <a href=\"../password/\">на эту кнопку</a>."))

    class Meta:
        model = User

        fields = ('game_nick', 'tel', 'password', 'is_active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'inputUsername',
                'placeholder': 'Введите логин'
            }))
    password = forms.CharField(
        label='Пароль:',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control border-end-0',
                'id': 'inputChoosePassword',
                'placeholder': 'Введите пароль'

            }))

    def clean(self):
        cleaned_data = super(CustomLoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином не зарегистрирован!')

        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError('Неверный пароль!')


class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control border-end-0',
            'id': 'inputChoosePassword',
            'placeholder': 'Введите пароль'

        }))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control border-end-0',
            'id': 'inputChoosePasswordConfirm',
            'placeholder': 'Введите пароль повторно'

        }))

    class Meta:
        model = User
        fields = ('tel', 'username', 'game_nick', 'avatar', 'whatsapp_boolean', 'telegram_boolean', 'viber_boolean',
                  'telegram_name',)  # 'full_name',)

        widgets = {
            'tel': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите телефон',
                'id': 'phone',
                'type': 'tel'

            }),
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите логин',
                'id': 'inputUserName'
            }),
            'game_nick': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите игровой ник',
                'id': 'inputGameNick'
            }),
            'avatar': TextInput(attrs={
                'type': 'file',
                'id': 'input__file',
                'class': 'input input__file',
                # 'style': 'display: none',

                'multiple': '',

            }),
            'whatsapp_boolean': TextInput(attrs={
                'type': 'checkbox',
                'class': 'form-check-input',
                'id': 'whatsapp',

            }),
            'telegram_boolean': TextInput(attrs={
                'type': 'checkbox',
                'class': 'form-check-input',
                'id': 'telegram',
                'data-bs-toggle': "modal",
                'data-bs-target': "#exampleModal"

            }),
            'viber_boolean': TextInput(attrs={
                'type': 'checkbox',
                'class': 'form-check-input',
                'id': 'viber',


            }),
            'telegram_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ник в telegram',
                'id': 'id_telegram_name',


            }),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if not avatar:
            avatar = 'avatar-default.png'
            return avatar

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True  # send confirmation email via signals
        user.tel = '+' + "".join(c for c in user.tel if c.isdecimal())
        user.avatar = self.cleaned_data.get("avatar")
        user.whatsapp_boolean = self.cleaned_data.get('whatsapp_boolean')
        user.is_active = True

        # obj = EmailActivation.objects.create(user=user)
        # obj.send_activation_email()
        if commit:
            user.save()
        return user
