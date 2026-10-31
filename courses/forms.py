from django import forms
from .models import Course, Topic


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "code", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["title", "weightage"]