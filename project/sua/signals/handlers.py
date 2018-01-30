from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from project.sua.models import Sua, Student, Application, Activity


@receiver(pre_save, sender=Sua, dispatch_uid="Sua_pre_save")
def Sua_pre_save_handler(sender, **kwargs):
    sua = kwargs['instance']
    print('handling sua save')
    if sua.is_valid:
        sua.update_student_suahours()
    else:
        if sua.added != 0.0:
            sua.clean_suahours()


@receiver(pre_delete, sender=Sua, dispatch_uid="Sua_pre_delete")
def Sua_pre_delete_handler(sender, **kwargs):
    sua = kwargs['instance']
    if sua.is_valid:
        sua.suahours = 0.0
        sua.update_student_suahours()


@receiver(post_delete, sender=Student, dispatch_uid="Student_post_delete")
def Student_post_delete_handler(sender, instance, *args, **kwargs):
    if instance.user:  # just in case user is not specified
        instance.user.delete()


@receiver(
    post_delete,
    sender=Application,
    dispatch_uid="Application_post_delete",
)
def Application_post_delete_handler(sender, instance, *args, **kwargs):
    if instance.sua:  # just in case user is not specified
        instance.sua.delete()
    if instance.proof:
        pf = instance.proof
        if pf.applications.count() == 0 and not pf.is_offline:
            instance.proof.delete()


@receiver(
    post_save,
    sender=Activity,
    dispatch_uid="Activity_post_save",
)
def Activity_post_save_handler(sender, instance, *args, **kwargs):
    for sua in instance.suas.all():
        if instance.is_valid:
            sua.is_valid = True
            sua.save()
        else:
            if not hasattr(sua, 'application') or not sua.application.is_checked:
                sua.is_valid = False
                sua.save()


# @receiver(
#     pre_delete,
#     sender=Activity,
#     dispatch_uid="Activity_pre_delete",
# )
# def Activity_pre_delete_handler(sender, instance, *args, **kwargs):
#     for sua in instance.suas.all():
#             sua.delete()
