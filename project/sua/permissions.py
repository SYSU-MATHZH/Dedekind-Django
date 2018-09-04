from rest_framework import permissions
from project.sua.models import Student


class IsTheStudentOrIsAdminUser(permissions.BasePermission):
    """
    Object-level permission to only allow the owner student to read it.
    Assumes the model instance has an `student` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.is_staff:
            return True
        elif isinstance(obj, Student):
            return obj.user == request.user
        elif hasattr(obj, 'student'):
            return obj.student.user == request.user
        elif hasattr(obj, 'owner'):
            return obj.owner == request.user
        else:
            assert hasattr(obj, 'owner')
            return False


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    要求登录，如果不是管理员则只读
    """

    def has_permission(self, request, view):

        if not (request.user and request.user.is_authenticated):
            return False

        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_staff
        )

class IsAdminUserOrActivity(permissions.BasePermission):

    def has_object_permission(self,request,view,obj):
#        print(obj.owner)
#        print(request.user)
        if not (request.user and request.user.is_authenticated):
            return False
        if (request.user.is_staff):
            return True
        if hasattr(request.user,'student'):
            if(request.user.student.power == 1 and obj.owner == request.user):
                return True

class IsAdminUserOrStudent(permissions.BasePermission):

    def has_object_permission(self,request,view,obj):

        if not (request.user and request.user.is_authenticated):
            return False
        if (request.user.is_staff):
            return True
        elif request.user.student == obj:
            return True

class IsTheStudentOrIsAdminUserOrActivity(permissions.BasePermission):

    def has_object_permission(self,request,view,obj):

        if not (request.user and request.user.is_authenticated):
            return False
        if (request.user.is_staff):
            return True
        elif request.user.student == obj:
            return True
        else:
            return request.user.student.power == 1
