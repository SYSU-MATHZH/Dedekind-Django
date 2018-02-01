from rest_framework import permissions
from project.sua.models import Student


class IsTheStudentOrIsAdminUser(permissions.BasePermission):
    """
    Object-level permission to only allow the owner student to read it.
    Assumes the model instance has an `student` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user:
            return False
        if request.user.is_staff:
            return True
        elif isinstance(obj, Student):
            return obj.user == request.user
        else:
            return obj.student.user == request.user
