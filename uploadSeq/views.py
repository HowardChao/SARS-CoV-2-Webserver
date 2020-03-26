from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.detail import DetailView
from . import forms

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
    if request.method == 'POST':
        myfile = request.FILES['fasta-file']
        print("myfile: ", myfile)
        form = forms.UploadFileForm(request.POST, request.FILES)
        print("form: ", form)
        print("Before form checking!! ", form.is_valid())
        if form.is_valid():
            print("After form checking!!")
            handle_uploaded_file(request.FILES['file'])
            # return HttpResponseRedirect('/success/url/')
    else:
        form = forms.UploadFileForm()
    return render(request, 'uploadSeq/upload_sequences_page.html', {'form': form})


def handle_uploaded_file(f):
    print("Writing out files!!")
    with open('~/Desktop/TRRRRY.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
