from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from department import serializers, models
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class DepartmentApiView(APIView):
    serializer_class = serializers.DepartmentSerializer
    permission_classes = [ IsAuthenticated ]
    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Department Created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request) -> Response:
        department_id = request.GET.get('department_id')
        try:
            if department_id is not None:
                data = models.Department.objects.get(id=department_id)
                serializer = serializers.DepartmentSerializer(data)
            else:
                data = models.Department.objects.all()
                serializer = serializers.DepartmentSerializer(data, many=True)

            return Response({'message': 'Department get successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        except models.Department.DoesNotExist:
            return Response({'message': 'Department Does not exist!'},status=status.HTTP_404_NOT_FOUND)
        

    def delete(self, request) -> Response:
        department_id = request.GET.get('department_id')
        if department_id:
            data = models.Department.objects.get(id=department_id)
            data.delete()
            return Response({'message': 'Department deleted successfully'}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    def put(self, request) -> Response:
        department_id = request.GET.get('department_id')
        try:
            if department_id is not None:
                data = models.Department.objects.get(id=department_id)
                serializer = serializers.DepartmentSerializer(data, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message': 'Department updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.Department.DoesNotExist:
            return Response({'message': 'Department Does not exist!'},status=status.HTTP_404_NOT_FOUND)

