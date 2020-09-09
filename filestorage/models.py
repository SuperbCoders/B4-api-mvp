from django.db import models

from filestorage.validators import filename_validator
from filestorage import consts
from filestorage.utils import file_upload_to, FileInfo


class APIFile(models.Model):
    # user = models.ForeignKey('core.User', related_name='api_files', on_delete=models.CASCADE)

    original_filename = models.CharField(max_length=255, blank=True, verbose_name='Имя файла', validators=[filename_validator])
    ext = models.CharField(max_length=255, blank=True, verbose_name='Расширение файла')

    file = models.FileField(upload_to=file_upload_to, verbose_name='Файл')
    file_type = models.CharField(max_length=255, choices=consts.FILE_TYPE_CHOICES, editable=False,
                                 verbose_name='Тип файла')
    file_sub_type = models.CharField(max_length=255, editable=False, blank=True, verbose_name='Подтип файла')
    file_duration = models.FloatField(blank=True, null=True, editable=False,
                                      verbose_name='Длительность файла (секунды)')

    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = ['-created_at']

    def __str__(self):
        return self.original_filename

    def save(self, *args, **kwargs):
        if self.file:
            data = FileInfo().get_data(self.file)
            self.file_type = data['type']
            self.file_sub_type = data['sub_type']
            self.file_duration = data['duration']
            self.original_filename = self.file.name
            self.full_clean()
            self.ext = self.original_filename.split('.')[-1]
        return super().save(*args, **kwargs)
