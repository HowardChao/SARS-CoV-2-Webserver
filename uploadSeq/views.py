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
    documents = models.Document.objects.all()
    example_fasta_covid_19_1 = "/media/example_fasta_files/covid_19.fasta"
    example_fasta_covid_19_2 = "/media/example_fasta_files/covid_19_2.fasta"
    if request.method == 'POST' and 'fasta-files-upload' in request.POST:
        form = forms.DocumentForm(request.POST, request.FILES)
        # print("form: ", form)
        # print("form.is_valid(): ", form.is_valid())
        if form.is_valid():
            doc = models.Document(fastafile = request.FILES['fastafile'])
            # print("request.FILES['fastafile']: ", request.FILES['fastafile'])
            fasta_file_content = request.FILES['fastafile'].read().decode("utf-8")
            doc.save()
            request.session['fasta_filename'] = request.FILES['fastafile'].name
            request.session['fasta_file_content'] = fasta_file_content
            return HttpResponseRedirect(reverse('uploadSeq-preview'))
            # return render(
            #     request,
            #     'uploadSeq/preview_sequences_page.html',
            #     {'example_fasta_1': example_fasta_covid_19_1, 'example_fasta_2': example_fasta_covid_19_2, 'fasta_filename': request.FILES['fastafile'], 'fasta_content': fasta_file_content, 'form': form}
            # )
    else:
        form = forms.DocumentForm()
    # for document in documents:
    #     document.delete()
    return render(
        request,
        'uploadSeq/upload_sequences_page.html',
        {'example_fasta_1': example_fasta_covid_19_1, 'example_fasta_2': example_fasta_covid_19_2, 'form': form}
    )
    # return JsonResponse({'tmp': ''})

def preview_file(request):
    example_fasta_covid_19_1 = "/media/example_fasta_files/covid_19.fasta"
    example_fasta_covid_19_2 = "/media/example_fasta_files/covid_19_2.fasta"
    fasta_filename = request.session['fasta_filename']
    fasta_file_content = request.session['fasta_file_content']
    # print("fasta_filename: ", fasta_filename)
    # print("fasta_file_content: ", fasta_file_content)
    return render(
        request,
        'uploadSeq/preview_sequences_page.html',
        {'example_fasta_1': example_fasta_covid_19_1, 'example_fasta_2': example_fasta_covid_19_2, 'fasta_filename': fasta_filename, 'fasta_file_content': fasta_file_content}
    )
