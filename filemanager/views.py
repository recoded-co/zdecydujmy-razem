__author__ = 'marcinra'


from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from filemanager.forms import DocumentForm
from django.views.generic import View
from filemanager.models import PostFileUpload
from django.core.urlresolvers import reverse
from django.template import RequestContext
from zr.models import Post
from django.core.servers.basehttp import FileWrapper
from zr.api import FileSerializer
from django.core.serializers import json
from django.views.decorators.csrf import csrf_exempt



class FileManager(View):

    def get(self, request, file_id):
        print "get " + file_id
        # Handle file download
        file = get_object_or_404(PostFileUpload, id = file_id)
        response = HttpResponse(FileWrapper(file.file), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename='+ file.name
        return response

    def post(self, request):

        # Handle file upload
        newfile = None
        if request.method == 'POST':
            print request.POST
            form = DocumentForm(request.POST, request.FILES)
            post = Post.objects.get(id = request.POST['post_id'])
            if form.is_valid() and post:
                newfile = PostFileUpload(file = request.FILES['datafile'], post = post, name=str(request.FILES['datafile']))
                newfile.save()
            # Redirect to the document list after POST

        #print "Response"
        #filedata = FileSerializer(newfile)

        #return HttpResponse(filedata.data, content_type='application/json')
        return HttpResponseRedirect(reverse('dashboard'))

@csrf_exempt
def angular_post(request):
    newfile = None
    if request.method == 'POST':
        print request.POST
        form = DocumentForm(request.POST, request.FILES)
        post = Post.objects.get(id = request.POST['post_id'])
        if form.is_valid() and post:
            newfile = PostFileUpload(file = request.FILES['datafile'], post = post, name=str(request.FILES['datafile']))
            newfile.save()
            # Redirect to the document list after POST

    print "Response angular_post"
    filedata = FileSerializer(newfile)
    return HttpResponse(filedata.data, content_type='application/json')