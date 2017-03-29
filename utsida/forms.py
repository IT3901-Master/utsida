from ajax_select import make_ajax_field
from ajax_select.fields import AutoCompleteField
from django import forms
from django.core.validators import URLValidator
from django.forms import ChoiceField
from django.forms.widgets import NumberInput
from .models import Query, University, CourseMatch, HomeCourse, AbroadCourse


class QueryCaseBaseForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ("homeInstitute", "continent", "country", "university",
                  "language", "academicQualityRating", "socialQualityRating",
                  "residentialQualityRating", "receptionQualityRating")
        widgets = {
            'academicQualityRating': NumberInput(attrs={'type': 'range', 'step': '1', 'max': '10', 'min': '1',
                                                        'value': '5', 'oninput': 'academicOutput.value=this.value'}),
            'socialQualityRating': NumberInput(attrs={'type': 'range', 'step': '1', 'max': '10', 'min': '1',
                                                      'value': '5', 'oninput': 'socialOutput.value=this.value'}),
            'residentialQualityRating': NumberInput(attrs={'type': 'range', 'step': '1', 'max': '10', 'min': '1',
                                                           'value': '5',
                                                           'oninput': 'residentialOutput.value=this.value'}),
            'receptionQualityRating': NumberInput(attrs={'type': 'range', 'step': '1', 'max': '10', 'min': '1',
                                                         'value': '5', 'oninput': 'receptionOutput.value=this.value'}),
        }

    def __init__(self, *args, **kwargs):
        super(QueryCaseBaseForm, self).__init__(*args, **kwargs)
        self.fields["homeInstitute"].required = False
        self.fields["continent"].required = False
        self.fields["continent"].widget.attrs.update({'id': 'continentField'})
        self.fields["continent"].widget.attrs.update({'onchange': 'filterCountries()'})
        self.fields["country"].required = False
        self.fields["country"].widget.attrs.update({'id': 'countryField'})
        self.fields["university"].required = False
        self.fields["language"].required = False
        self.fields["academicQualityRating"].required = False
        self.fields["socialQualityRating"].required = False
        self.fields["residentialQualityRating"].required = False
        self.fields["receptionQualityRating"].required = False


class DateInput(forms.DateInput):
    input_type = 'date'


class CourseMatchForm(forms.ModelForm):
    class Meta:
        model = CourseMatch
        fields = ['abroadCourse', 'homeCourse', 'comment', 'approval_date', 'approved', ]
        widgets = {
            'approval_date': DateInput()
        }

    homeCourse = AutoCompleteField('homeCourseFind', help_text=None, required=True,
                                   attrs={"placeholder": "Søk på fagnavn/kode"})

    abroadCourse = AutoCompleteField('abroadCourseFind', help_text=None, required=True,
                                     attrs={"placeholder": "søk på fagnavn/kode"})

    def save(self, commit=True):
        courseMatch = super(CourseMatchForm, self).save(commit=False)
        CourseMatch.approved = self.cleaned_data['approved']
        CourseMatch.approval_date = self.cleaned_data['approval_date']
        CourseMatch.comment = self.cleaned_data['comment']
        if commit:
            courseMatch.save()

        return courseMatch


class abroadCourseForm(forms.ModelForm):
    class Meta:
        model = AbroadCourse
        fields = ['code', 'name', 'university', 'description_url', 'study_points']
        widgets = {
            'code': forms.TextInput(
                attrs={'id': 'add-form-code', 'required': True, 'placeholder': 'Legg til fag-kode...'}
            ),
            'name': forms.TextInput(
                attrs={'id': 'add-form-name', 'required': True, 'placeholder': 'Legg til fag-navn...'}
            ),
            'description_url': forms.URLInput(
                attrs={'id': 'add-form-url', 'required': False, 'placeholder': 'Legg til fag-url...',
                       "pattern": "https?://.+"}
            ),
            'study_points': forms.NumberInput(
                attrs={'id': 'add-form-study-points', 'required': False, 'placeholder': 'Legg til antall studiepoeng'}
            ),
            'university': forms.Select(attrs={'id': 'add-form-university', 'required': True,
                                                        'placeholder': 'Legg til antall studiepoeng'}
                                                 ),
        }
