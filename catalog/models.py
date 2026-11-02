import uuid

from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator


class Genre(models.Model):
    """Модель жанра книги."""
    name = models.CharField('Название жанра', max_length=200, 
                            help_text='Введите жанр книги')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Возвращает URL для доступа к детальной странице жанра."""
        return reverse('genre-detail', args=[str(self.id)])


class Language(models.Model):
    """Модель языка книги."""
    name = models.CharField('Название языка', max_length=200,
                            help_text='Введите язык книги')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Возвращает URL для доступа к детальной странице языка."""
        return reverse('language-detail', args=[str(self.id)])


class Author(models.Model):
    """Модель автора."""
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    date_of_birth = models.DateField('Дата рождения', null=True, blank=True)
    date_of_death = models.DateField('Дата смерти', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        """Возвращает URL для доступа к детальной странице автора."""
        return reverse('author-detail', args=[str(self.id)])


class Book(models.Model):
    """Модель книги."""
    title = models.CharField('Название', max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, 
                               verbose_name='Автор')
    summary = models.TextField('Краткое описание', max_length=1000, 
                               help_text='Введите краткое описание книги')
    isbn = models.CharField('ISBN', max_length=13, 
                            help_text='13 цифр ISBN номера',
                            validators=[RegexValidator(
                                regex=r'^\d{13}$',
                                message='ISBN должен содержать ровно 13 цифр'
                            )])
    genre = models.ManyToManyField(Genre, help_text='Выберите жанры',
                                   verbose_name='Жанр')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True,
                                 verbose_name='Язык')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Возвращает URL для доступа к детальной странице книги."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Создаёт строку со списком жанров для админки."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Жанр'


class BookInstance(models.Model):
    """Модель экземпляра книги."""
    LOAN_STATUS = (
        ('m', 'На обслуживании'),
        ('o', 'Доступна'),
        ('a', 'Зарезервирована'),
        ('r', 'Выдана'),
    )

    id = models.UUIDField('ID экземпляра', primary_key=True, default=uuid.uuid4,
                          help_text='Уникальный ID экземпляра')
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True,
                             verbose_name='Книга')
    imprint = models.CharField('Издание', max_length=200)
    due_back = models.DateField('Дата возврата', null=True, blank=True)
    status = models.CharField('Статус', max_length=1, choices=LOAN_STATUS, 
                              blank=True, default='m', help_text='Статус доступности')
    borrower = models.ForeignKey('auth.User', on_delete=models.SET_NULL, 
                                 null=True, blank=True, verbose_name='Читатель')

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title if self.book else "Без названия"})'

    def get_absolute_url(self):
        """Возвращает URL для доступа к детальной странице экземпляра книги."""
        return reverse('bookinstance-detail', args=[str(self.id)])