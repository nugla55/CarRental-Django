from django import forms
from datetime import date
from calendar import monthrange


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


class PaymentForm(forms.Form):
    number = forms.IntegerField(required=True, label="Card Number", widget=forms.TextInput(attrs={'size': '16'}))
    first_name = forms.CharField(required=True, label="Card Holder First Name", max_length=30)
    last_name = forms.CharField(required=True, label="Card Holder Last Name", max_length=30)
    expire_month = forms.ChoiceField(required=True, choices=[(x, x) for x in range(1, 13)])
    expire_year = forms.ChoiceField(required=True,
                                    choices=[(x, x) for x in range(date.today().year, date.today().year + 15)])
    cvv_number = forms.IntegerField(required=True, label="CVV Number", widget=forms.TextInput(attrs={'size': '3'}))

    def init(self, *args, **kwargs):
        self.payment_data = kwargs.pop('payment_data', None)
        super(PaymentForm, self).init(*args, **kwargs)

    def clean(self):
        cleaned_data = super(PaymentForm, self).clean()
        cvv_number = cleaned_data.get('cvv_number')
        number = cleaned_data.get('number')
        expire_month = cleaned_data.get('expire_month')
        expire_year = cleaned_data.get('expire_year')
        year = int(expire_year)
        month = int(expire_month)
        # find last day of the month
        day = monthrange(year, month)[1]
        expire = date(year, month, day)

        if len(str(number)) != 16:
            self.errors["number"] = self.error_class(["The credit card number is wrong!"])

        if len(str(cvv_number)) != 3:
            self.errors['cvv_number'] = self.error_class(["The cvv card number is wrong!"])

        if date.today() > expire:
            # raise forms.ValidationError("The expiration date you entered is in the past.")
            self._errors["expire_year"] = self.error_class(["The expiration date you entered is in the past."])

        return cleaned_data
