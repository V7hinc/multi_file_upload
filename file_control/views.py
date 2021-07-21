from django.shortcuts import render

# Create your views here.
import os
from django.shortcuts import render, HttpResponse
from multi_file_upload.settings import BASE_DIR
UPLOAD_PATH = os.path.join(BASE_DIR, 'upload_dir')
if not os.path.isdir(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)

# Create your views here.


def files_upload(request):
    if request.method == 'GET':
        return render(request, 'filesupload.html')
    elif request.is_ajax():
        # 根据input框的name属性值取到文件对象
        files = request.FILES.getlist('files')
        for file in files:
            # 获取文件名，文件对象的__str__属性返回的是文件名
            file_name = str(file)
            with open(os.path.join(UPLOAD_PATH, file_name), 'wb') as f:
                # 分块写入，防止大文件卡死
                for chunk in file.chunks(chunk_size=2014):
                    f.write(chunk)
        return HttpResponse('ajaxOK')
    elif request.method == 'POST':
        '''
        保存上传文件前，数据需要存放在某个位置。默认当上传文件小于2.5M时，django会将上传文件的全部内容读进内存。从内存读取一次，写磁盘一次。
        但当上传文件很大时，django会把上传文件写到临时文件中，然后存放到系统临时文件夹中。
        :param request:
        :return:
        '''
        # 从请求的FILES中获取上传文件的文件名，file为页面上type=files类型input的name属性值
        filename = request.FILES['upload_files'].name
        abs_filename = os.path.join(UPLOAD_PATH, filename)
        # 在项目目录下新建一个文件
        with open(abs_filename, 'wb') as f:
            # 从上传的文件对象中一点一点读
            for chunk in request.FILES['upload_files'].chunks():
                # 写入本地文件
                f.write(chunk)
        return HttpResponse('上传ok')