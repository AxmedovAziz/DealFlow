# forms.py
from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["name", "bio", "image", "phone"]
        widgets = {
            "image": forms.ClearableFileInput(
                attrs={"class": "image-input", "accept": "image/*"}
            ),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_image(self):
        image = self.cleaned_data.get("image", False)
        if not image:
            return "profile_pics/default-profile.png"
        return image
