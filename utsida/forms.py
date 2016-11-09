from django import forms

from .models import Query, University


class QueryCaseBaseForm(forms.ModelForm):

    class Meta:
        model = Query
        fields = ("homeInstitute", "continent", "country", "university",
                  "language", "academicQualityRating", "socialQualityRating")

    def __init__(self, *args, **kwargs):
        super(QueryCaseBaseForm, self).__init__(*args, **kwargs)
        self.fields["homeInstitute"].required = False
        self.fields["continent"].required = False
        self.fields["continent"].widget.attrs.update({'id': 'continentField'})
        self.fields["country"].required = False
        self.fields["country"].widget.attrs.update({'id': 'countryField'})
        self.fields["university"].required = False
        self.fields["language"].required = False
        self.fields["academicQualityRating"].required = False
        self.fields["socialQualityRating"].required = False


class University_selection_form(forms.ModelForm):

    class Meta:
        model = University
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(University_selection_form, self).__init__(*args,**kwargs)
        self.fields["name"].required = True
