from django import forms

from .models import Court


class NameForm(forms.Form):
    years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
    court = forms.ModelChoiceField(queryset=Court.objects.all(), required=False)
    date_pron_from = forms.DateField(label='Date pronounced from',
                                     widget=forms.SelectDateWidget(years=years, empty_label=("Year", "Month", "Day")),
                                     initial=None, required=False)
    date_created_from = forms.DateField(label='Date created from',
                                        widget=forms.SelectDateWidget(years=years,
                                                                      empty_label=("Year", "Month", "Day")),
                                        initial=None, required=False)
    date_published_from = forms.DateField(label='Date published from',
                                          widget=forms.SelectDateWidget(years=years,
                                                                        empty_label=("Year", "Month", "Day")),
                                          initial=None, required=False)
    date_pron_to = forms.DateField(label='Date pronounced to',
                                   widget=forms.SelectDateWidget(years=years, empty_label=("Year", "Month", "Day")),
                                   initial=None, required=False)
    date_created_to = forms.DateField(label='Date created to',
                                      widget=forms.SelectDateWidget(years=years, empty_label=("Year", "Month", "Day")),
                                      initial=None, required=False)
    date_published_to = forms.DateField(label='Date published to',
                                        widget=forms.SelectDateWidget(years=years,
                                                                      empty_label=("Year", "Month", "Day")),
                                        initial=None, required=False)

    file_name = forms.CharField(label="File name", required=False, widget=forms.TextInput(attrs={'size': '120'}))
    file_type = forms.ChoiceField(label="Type", choices=(
        ('', '-----'),
        ("Civil", "Civil"),
        ("Penal", "Penal"),
        ("Contravention", "Contravention")), required=False)
    file_theme = forms.CharField(label="Theme", required=False, widget=forms.TextInput(attrs={'size': '120'}))
    file_content = forms.CharField(label="Content of the decision", required=False,
                                   widget=forms.TextInput(attrs={'size': '120'}))
