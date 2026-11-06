from django import forms
from django.core.exceptions import ValidationError
import datetime


class RenewBookForm(forms.Form):
    """Форма для продления срока возврата книги."""
    renewal_date = forms.DateField(
        help_text="Введите дату между сегодня и 4 неделями (по умолчанию 3).",
        label="Дата продления"
    )

    def clean_renewal_date(self):
        """Проверка введённой даты — она должна быть в будущем."""
        data = self.cleaned_data['renewal_date']
        if data < datetime.date.today():
            raise ValidationError('Дата не может быть в прошлом')
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError('Дата не может быть более чем на 4 недели в будущем')
        return data