# -*- coding: utf-8 -*-
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
from rest_framework.renderers import JSONRenderer


class FileManager(View):

    def get(self, request, file_id):
        # Handle file download
        file = get_object_or_404(PostFileUpload, id = file_id)
        response = HttpResponse(FileWrapper(file.file), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename='+ file.name.encode('utf-8')
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
        return HttpResponseRedirect(reverse('dashboard'))

@csrf_exempt
def angular_post(request):
    newfile = None
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        post = Post.objects.get(id = request.POST['post_id'])

        if request.user != post.author:
            return HttpResponse({}, content_type='application/json')

        if form.is_valid() and post:
            newfile = PostFileUpload(file = request.FILES['datafile'], post = post, name=str(request.FILES['datafile']))
            newfile.save()

    if newfile:
        filedata = FileSerializer(newfile)
        return HttpResponse(JSONRenderer().render(filedata.data), content_type='application/json')
    else:
        return HttpResponse({}, content_type='application/json')
