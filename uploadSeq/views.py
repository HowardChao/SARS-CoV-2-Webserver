from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.detail import DetailView

class BasicUploadView(DetailView):
    def get(self, request):
        return render(self.request, "uploadSeq/upload_sequences_page.html", {
        })

    def post(self, request):
        if 'samples-files-upload' in request.POST:
            myfile = request.FILES['samples-files-selected']
            print("myfile.name: ", myfile.name)
            fs = FileSystemStorage()
            if os.path.exists(os.path.join(base_dir, myfile.name)):
                os.remove(os.path.join(base_dir, myfile.name))
            filename = fs.save(os.path.join(base_dir, myfile.name), myfile)
            # Start checking files
            (samples_txt_file_name, samples_list_key, sample_list, sample_file_validity, sample_file_two_or_one) = utils_func.check_samples_txt_file(base_dir)
            check_uploaded_fastq_file_ans = utils_func.check_uploaded_fastq_file(project_name, email, analysis_code)
            check_uploaded_fastq_file_whole_ans = utils_func.check_uploaded_fastq_file_whole_answer(check_uploaded_fastq_file_ans)
            # Url needs to be updated one file is uploaded!!
            uploaded_sample_file_url = utils_func.get_sample_file_url(project_name, email, analysis_code)
            return render(request, "uploadSeq/upload_sequences_page.html", {
                'project_name': project_name,
                'analysis_code': analysis_code,
                'email': email,
                'assembly_type_input': assembly_type_input,
                'samples_txt_file_name': samples_txt_file_name,
                'samples_list_key': samples_list_key,
                'sample_list': sample_list,
                'sample_file_validity': sample_file_validity,
                'sample_file_two_or_one': sample_file_two_or_one,
                'check_uploaded_fastq_file_ans': check_uploaded_fastq_file_ans,
                'check_uploaded_fastq_file_whole_ans': check_uploaded_fastq_file_whole_ans,
                'uploaded_sample_file_url': uploaded_sample_file_url,
                'one_group_samples_csv': one_group_samples_csv,
                'two_group_samples_csv': two_group_samples_csv,
                'fastq_R1': fastq_R1,
                'fastq_R2': fastq_R2,
            })
        elif 'remove-samples-file' in request.POST:
            print("remove-samples-file!!!")
            fs = FileSystemStorage()
            if fs.exists(base_dir):
                shutil.rmtree(base_dir)
            destination_QC_html_dir = os.path.join(os.path.dirname(__file__), 'templates', 'dataanalysis', 'tmp', project_name + '_' + email + '_' + analysis_code)
            if os.path.exists(destination_QC_html_dir):
                shutil.rmtree(destination_QC_html_dir)
            # Start checking files
            (samples_txt_file_name, samples_list_key, sample_list, sample_file_validity, sample_file_two_or_one) = utils_func.check_samples_txt_file(base_dir)
            new_task_name = project_name + email + analysis_code
            print("#############")
            print("#####  Delete new_task_name ######")
            targetCeleryTask = TaskResult.objects.filter(task_id = project_name + email + analysis_code)
            print("***targetCeleryTask ", targetCeleryTask, " : ", targetCeleryTask.exists())
            if targetCeleryTask.exists():
                targetCeleryTask.delete()
            check_uploaded_fastq_file_ans = utils_func.check_uploaded_fastq_file(project_name, email, analysis_code)
            check_uploaded_fastq_file_whole_ans = utils_func.check_uploaded_fastq_file_whole_answer(check_uploaded_fastq_file_ans)
            uploaded_sample_file_url = utils_func.get_sample_file_url(project_name, email, analysis_code)
            return render(request, "dataanalysis/file_upload.html", {
                'project_name': project_name,
                'analysis_code': analysis_code,
                'email': email,
                'assembly_type_input': assembly_type_input,
                'samples_txt_file_name': samples_txt_file_name,
                'samples_list_key': samples_list_key,
                'sample_list': sample_list,
                'sample_file_validity': sample_file_validity,
                'sample_file_two_or_one': sample_file_two_or_one,
                'check_uploaded_fastq_file_ans': check_uploaded_fastq_file_ans,
                'check_uploaded_fastq_file_whole_ans': check_uploaded_fastq_file_whole_ans,
                'uploaded_sample_file_url': uploaded_sample_file_url,
                'one_group_samples_csv': one_group_samples_csv,
                'two_group_samples_csv': two_group_samples_csv,
                'fastq_R1': fastq_R1,
                'fastq_R2': fastq_R2,
            })
        elif 'multi_samples_workflow_setup_button' in request.POST:
            (samples_txt_file_name, samples_list_key, sample_list, sample_file_validity, sample_file_two_or_one) = utils_func.check_samples_txt_file(base_dir)
            # if assembly_type_input
            if assembly_type_input == "de_novo_assembly":
                template_html = "dataanalysis/analysis_home_denovo.html"
                return redirect((reverse('de_novo_assembly_dataanalysis_home', kwargs={'slug_project': url_parameter})))
            elif assembly_type_input == "reference_based_assembly":
                template_html = "dataanalysis/analysis_home_reference_based.html"
                return redirect((reverse('reference_mapping_dataanalysis_home', kwargs={'slug_project': url_parameter})))
            elif assembly_type_input == "virus_assembly":
                template_html = "dataanalysis/analysis_home_virus.html"
                return redirect((reverse('virus_dataanalysis_home', kwargs={'slug_project': url_parameter})))
            return render(request, template_html, {
                'project_name': project_name,
                'analysis_code': analysis_code,
                'email': email,
                'assembly_type_input': assembly_type_input,
                'samples_txt_file_name': samples_txt_file_name,
                'samples_list_key': samples_list_key,
                'sample_list': sample_list,
                'sample_file_validity': sample_file_validity,
                'sample_file_two_or_one': sample_file_two_or_one,
                'check_uploaded_fastq_file_ans': check_uploaded_fastq_file_ans,
                'check_uploaded_fastq_file_whole_ans': check_uploaded_fastq_file_whole_ans,
                'uploaded_sample_file_url': uploaded_sample_file_url,
                'one_group_samples_csv': one_group_samples_csv,
                'two_group_samples_csv': two_group_samples_csv,
                'fastq_R1': fastq_R1,
                'fastq_R2': fastq_R2,
            })
        myfile = request.FILES['file_choose']
        fs = FileSystemStorage()
        print("myfilemyfilemyfile: ", myfile)
        # Sample name!
        (samples_txt_file_name, samples_list_key, sample_list, sample_file_validity, sample_file_two_or_one) = utils_func.check_samples_txt_file(base_dir)
        for sample in sample_list:
            if not fs.exists(os.path.join(base_dir, 'Uploaded_files', sample)):
                os.makedirs(os.path.join(base_dir, 'Uploaded_files', sample))
                # Found split sample name
            file_name_tmp_1 = myfile.name.replace(".R1.fastq.gz", "")
            file_name_tmp_2 = file_name_tmp_1.replace(".R2.fastq.gz", "")
            if file_name_tmp_2 == sample:
                filename = fs.save(os.path.join(base_dir, "Uploaded_files", sample, myfile.name), myfile)
                uploaded_file_url = fs.url(filename)
        check_uploaded_fastq_file_ans = utils_func.check_uploaded_fastq_file(project_name, email, analysis_code)
        check_uploaded_fastq_file_whole_ans = utils_func.check_uploaded_fastq_file_whole_answer(check_uploaded_fastq_file_ans)
        data = {
            'project_name': project_name,
            'analysis_code': analysis_code,
            'email': email,
            'assembly_type_input': assembly_type_input,
            'samples_txt_file_name': samples_txt_file_name,
            'samples_list_key': samples_list_key,
            'sample_list': sample_list,
            'sample_file_validity': sample_file_validity,
            'sample_file_two_or_one': sample_file_two_or_one,
            'check_uploaded_fastq_file_ans': check_uploaded_fastq_file_ans,
            'check_uploaded_fastq_file_whole_ans': check_uploaded_fastq_file_whole_ans,
            'uploaded_sample_file_url': uploaded_sample_file_url,
            'one_group_samples_csv': one_group_samples_csv,
            'two_group_samples_csv': two_group_samples_csv,
            'fastq_R1': fastq_R1,
            'fastq_R2': fastq_R2,
            }
        return JsonResponse(data)
