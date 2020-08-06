import os
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
# 在django的conf里面导入setting，通过这个setting就能拿到全局配置信息
from django.conf import settings
from django.http.response import StreamingHttpResponse
from django.utils.encoding import escape_uri_path
# 导入查询集
from .models import Reports
# 导入序列化器类
from .serializers import ReportsModelSerializer
# 导入文件流生成器
from utils.utils import get_file_content

class ReportsViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsModelSerializer
    # 指定认证
    permission_classes =[permissions.IsAuthenticated]
    # 指定排序字段
    ordering_fields=['id','name']
    # 获取环境变量的名称和id


    # def list(self, request, *args, **kwargs):
    #     pass
    #
    # def retrieve(self, request, *args, **kwargs):
    #     pass


    @action(detail=True)
    def download(self, request, *args, **kwargs):
        # 获取html源码：通过获取报告的模型对象获取
        instance = self.get_object()
        # 在instance的html字段里面
        html = instance.html
        # 数据库中报告的文件名
        name = instance.name

        # 获取测试报告所属目录路径
        # 获取目录路径的方式有：①字典获取值得方式获取②通过属性的方式获取
        report_dir = settings.REPORT_DIR

        # 生成html文件，存放到reports目录下
        report_full_dir = os.path.join(report_dir, name) + '.html'
        # 判断当前文件名是否存在，如果不存在，则将测试报告保存在report目录下；如果存在，则不保存
        if not os.path.exists(report_full_dir):
            with open(report_full_dir, 'w', encoding='utf-8') as file:
                file.write(html)

        # 获取文件流，返回给前端
        # 创建一个生成器，获取文件流，每次获取的是文件字节数据
        response = StreamingHttpResponse(get_file_content(report_full_dir))

        # 解决文件名为中文的时候出现乱码的问题
        # escape_uri_path：将文件名进行编码
        html_file_name = escape_uri_path(name + '.html')

        # 添加响应头：下载文件的响应头添加方式如下
        # 直接使用Response对象['响应头名称'] = '值'
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f"attachement; filename*=UTF-8''{html_file_name}"

        # return StreamingHttpResponse(get_file_content(report_full_dir))
        return response