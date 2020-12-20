from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

# �����ѯ��
from .models import Envs
# �������л�����
from .serializers import EnvsModelSerializer,EnvsNamesSerializer
class EnvsViewSet(ModelViewSet):
    # ��ѯ��
    queryset = Envs.objects.all()
    # ���л�����
    serializer_class = EnvsModelSerializer
    # ָ����֤
    permission_classes =[permissions.IsAuthenticated]
    # ָ�������ֶ�
    ordering_fields=['id','name']
    # ��ȡ�������������ƺ�id

    # detail���Ҫ�����id������ΪTrue���������id������ΪFalse
    @action(detail=False)
    def names(self,request, *args, **kwargs):
        # ��ȡ��ѯ��
        qs=self.get_queryset()
        return Response(self.get_serializer(qs,many=True).data)
        # ��ע����Ϊ�ж�������������Ҫ����many=True

    # ��дget_serializer_class
    def get_serializer_class(self):
        # if self.action=='names':
        #     return EnvsNamesSerializer
        # else:
        #     # �������л�����
        #     return self.serializer_class

        # ��������Ŀд��
        return EnvsNamesSerializer if self.action == 'names' else  self.serializer_class
