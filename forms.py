from django import forms
from app.models import TODO

class TODOForm(forms.ModelForm):
    due_date = forms.DateField(required=False, widget=forms.DateInput(attrs={
        "type": "date", "class": "form-control"
    }))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "rows": 3, "class": "form-control", "placeholder": "Add details (optional)"
    }))
    class Meta:
        model = TODO
        fields = ['title', 'description', 'due_date', 'status', 'priority', 'category']
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Task title"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "priority": forms.Select(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }
