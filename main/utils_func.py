import os
import uuid
from django.conf import settings

########################
### Checking session ###
########################
def analysis_code_generator():
    return uuid.uuid1().hex

def check_session(request):
    analysis_code = None
    if 'analysis_code' in request.session:
        analysis_code = request.session['analysis_code']
        print("analysis_code: ", analysis_code)
        request.session["analysis_code"] = analysis_code
    return analysis_code

def create_sample_directory(analysis_code):
    datadir = os.path.join(settings.MEDIA_ROOT, 'tmp', analysis_code)
    os.makedirs(datadir)
