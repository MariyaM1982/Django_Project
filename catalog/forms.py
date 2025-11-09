from django import forms
from .models import Product
from django.core.exceptions import ValidationError
import os



# Список запрещённых слов (в любом регистре)
BANNED_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]

# Максимальный размер файла: 5 МБ = 5 * 1024 * 1024 байт
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 МБ
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/jpg']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'preview', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы Bootstrap ко всем полям
        placeholders = {
            'name': 'Введите название продукта',
            'description': 'Описание продукта',
            'price': 'Цена в рублях',
        }

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(field_name, f'Введите {field.label.lower()}')
            })

        # Для поля preview — отдельный класс (можно и без form-control, но пусть будет)
        if 'preview' in self.fields:
            self.fields['preview'].widget.attrs.update({
                'class': 'form-control-file'
            })

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            if self.contains_banned_word(name):
                raise forms.ValidationError("Название содержит запрещённые слова.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description:
            if self.contains_banned_word(description):
                raise forms.ValidationError("Описание содержит запрещённые слова.")
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_preview(self):
        image = self.cleaned_data.get('preview')
        if image:
            # Проверка размера файла
            if image.size > MAX_UPLOAD_SIZE:
                raise ValidationError(
                    f"Размер изображения не должен превышать {MAX_UPLOAD_SIZE / (1024 * 1024):.1f} МБ.")

            # Проверка формата по content_type
            if image.content_type not in ALLOWED_IMAGE_TYPES:
                raise ValidationError("Разрешены только форматы: JPEG и PNG.")

            # Дополнительная проверка расширения (на всякий случай)
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise ValidationError("Недопустимое расширение файла. Разрешены: .jpg, .jpeg, .png.")

        return image

    def contains_banned_word(self, text):
        """Проверяет, содержит ли текст запрещённые слова (без учёта регистра)"""
        text_lower = text.lower()
        return any(word in text_lower for word in BANNED_WORDS)