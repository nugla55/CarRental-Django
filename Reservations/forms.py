from django import forms


class FilteredListCars(forms.Form):
    takeDate = forms.DateTimeField(label="Pick Up Date",
                                   widget=forms.DateTimeInput(attrs={
                                       "type": "datetime-local", "name": "tookDate", "id": "first", "min": "",
                                       "class": "form-control datepicker px-3"
                                   })
                                   )
    returnDate = forms.DateTimeField(label="Pick Off Date",
                                     widget=forms.DateTimeInput(attrs={
                                         "type": "datetime-local", "name": "tookDate", "id": "second",
                                         "class": "form-control datepicker px-3"
                                     })
                                     )
    branches = (
        ("Adana", "Adana"),
        ("İstanbul", "İstanbul"),
    )
    branch = forms.ChoiceField(choices=branches)