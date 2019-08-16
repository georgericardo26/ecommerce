from main.models import LogSystem
from django.contrib.admin.models import ADDITION, LogEntry
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.contenttypes.models import ContentType
from django.utils import six
from django.utils.encoding import force_text


class ActionsForLogEntry:

    def insert_log_entry(self, request, instance, validated_data, action, serializer_name):

        try:
            action_string = "Added" if action == 1 else "Changed" if action == 2 else "Deleted"
            message = []

            if instance.pk:
                message = [
                    '%(action)s %(name)s "%(object)s".' % {
                        'action': action_string,
                        'name': force_text(instance._meta.verbose_name),
                        'object': force_text(instance)
                    }
                ]
                LogSystem.objects.log_action(
                    user_id=request.user.pk,
                    content_type_id=ContentType.objects.get_for_model(instance).pk,
                    object_id=instance.pk,
                    object_repr=serializer_name,
                    action_flag=action,
                    change_message=message,
                )

        except Exception:
            pass