from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.detail import DetailView
from django.template import RequestContext
from . import forms
from . import models

# class BasicUploadView(DetailView):
#     def get(self, request):
#         return render(self.request, "uploadSeq/upload_sequences_page.html", {
#         })
#
#     def post(self, request):
#         form = UploadFileForm(request.POST, request.FILES)
#             if form.is_valid():
#                 instance = ModelWithFileField(file_field=request.FILES['file'])
#                 instance.save()
#         return render(request, 'uploadSeq/upload_sequences_page.html', {'form': form})

def upload_file(request):
    if request.method == 'POST' and 'fasta-files-upload' in request.POST:
        form = forms.DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = models.Document(fastafile = request.FILES['fastafile'])
            doc.save()
    else:
        form = forms.DocumentForm()
    return render(
        request,
        'uploadSeq/upload_sequences_page.html',
        {'form': form}
    )
