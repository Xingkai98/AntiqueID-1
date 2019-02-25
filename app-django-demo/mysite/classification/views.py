from django.shortcuts import render, redirect
import os
import json
from django.http import HttpResponse,JsonResponse
from . import img_loader as ld
import numpy as np
import tensorflow as tf
# Create your views here.
size = 600,600

def index(request):
    return render(request, 'classification/intro.html')

def color_mind(request):
    return render(request, 'classification/color_mind.html')

def result(request):
    return render(request, 'classification/intro2.html')

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return render(request, 'classification/logout.html')
    request.session.flush()
    return render(request, 'classification/logout.html')

def handle_uploaded_file(f):
    with open('test/name.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload_file(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        #这里的img是h5表单里的name
        Dict = {}
        myFile = request.FILES.get("imageFile", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")
        path = os.path.join(os.getcwd(), myFile.name)
        print(path)
        #path = os.path.join(os.path.dirname(os.path.realpath(path)))
        pic = ld.transform_pic(path, size)
        pic = pic.reshape([1,600,600,3])
        pic = tf.convert_to_tensor(pic)
        Dict['path'] = path
        print(path)
        print(pic)
        destination = open(path, 'wb')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        #locals代表所有数据传入render中的页面
        return render(request, "classification/result.html", locals())
        #用json模块将python的字典转为json格式以便js读取
        #return render(request, "classification/result.html", {'Dict':json.dumps(Dict)})
        #return HttpResponse("upload over!")

