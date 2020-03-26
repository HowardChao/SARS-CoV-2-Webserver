from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic.detail import DetailView
from django.template import RequestContext
from django.urls import reverse
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
    if request.method == 'POST' and 'fasta-files-upload-modal' in request.POST:
        form = forms.DocumentForm(request.POST, request.FILES)
        print("form: ", form)
        print("form.is_valid(): ", form.is_valid())
        if form.is_valid():
            doc = models.Document(fastafile = request.FILES['fastafile'])
            doc.save()
            return HttpResponseRedirect(reverse('uploadSeq-upload'))
    else:
        form = forms.DocumentForm()
    documents = models.Document.objects.all()
    # for document in documents:
    #     document.delete()
    return render(
        request,
        'uploadSeq/upload_sequences_page.html',
        {'documents': documents, 'form': form}
    )
    # return JsonResponse({'tmp': ''})
