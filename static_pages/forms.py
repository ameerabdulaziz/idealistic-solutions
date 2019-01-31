from django import forms
from static_pages.models import StaticPages
from ckeditor.widgets import CKEditorWidget


class StaticPageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StaticPageForm, self).__init__(*args, **kwargs)
        self.fields['page_title'].widget = forms.TextInput(attrs={"type":"text","class":"form-control",'id':"inputText"})
        self.fields['meta_description'].widget = forms.TextInput(attrs={"type":"text","class":"form-control",'id':"inputText"})
        self.fields['meta_keywords'].widget = forms.TextInput(attrs={"type":"text","class":"form-control",'id':"inputText"})
        self.fields['meta_author'].widget = forms.TextInput(attrs={"type":"text","class":"form-control",'id':"inputText"})
        self.fields['created_by'].widget = forms.HiddenInput()
        self.fields['updated_by'].widget = forms.HiddenInput()
        # self.fields['active'].widget = forms.CheckboxInput(attrs={"class":"checkbox checkbox__custom checkbox__style1"})
        self.fields['published_date'].widget = forms.DateTimeInput(attrs={"type":"text"})

    class Meta():
        model = StaticPages
        exclude = ['slug']
