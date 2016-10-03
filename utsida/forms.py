from django import forms

from .models import Query


class QueryCaseBaseForm(forms.ModelForm):

    class Meta:
        model = Query
        fields = ("homeInstitute", "country", "university", "studyPeriod",
                  "language", "academicQualityRating", "socialQualityRating")

    def __init__(self, *args, **kwargs):
        super(QueryCaseBaseForm, self).__init__(*args, **kwargs)
        self.fields["homeInstitute"].required = False
        self.fields["country"].required = False
        self.fields["university"].required = False
        self.fields["studyPeriod"].required = False
        self.fields["language"].required = False
        self.fields["academicQualityRating"].required = False
        self.fields["socialQualityRating"].required = False




