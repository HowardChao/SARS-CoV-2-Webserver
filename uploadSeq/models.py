from django.db import models

class Document(models.Model):
    fastafile = models.FileField(upload_to='fasta_files/')
