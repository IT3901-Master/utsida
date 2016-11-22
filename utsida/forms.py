from datetime import date

from ajax_select import make_ajax_field
from ajax_select.fields import AutoCompleteSelectField
from django import forms

from .models import Query, University, CourseMatch, HomeCourse


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


class DateInput(forms.DateInput):
    input_type = 'date'

class CourseMatchForm(forms.ModelForm):


    class Meta:
        model = CourseMatch
        fields = ['abroadCourse','homeCourse','comment','approval_date','approved',]
        widgets = {
            'approval_date': DateInput()
        }

    homeCourse = make_ajax_field(CourseMatch, 'homeCourse', 'homeCourseFind', show_help_text=False, required=False)

    def save(self, commit=True):
        courseMatch = super(CourseMatchForm, self).save(commit=False)
        CourseMatch.approved = self.cleaned_data['approved']
        CourseMatch.approval_date = self.cleaned_data['approval_date']
        CourseMatch.comment = self.cleaned_data['comment']
        if commit:
            courseMatch.save()

        return courseMatch


