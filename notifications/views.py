from push_notifications.api.rest_framework import GCMDeviceViewSet


class FCMDeviceViewSet(GCMDeviceViewSet):

    def perform_create(self, serialiazer):
        user = self.request.user
        if user.is_authenticated:
            serialiazer.save(user=user, cloud_message_type='FCM')
        return super(FCMDeviceViewSet, self).perform_create(serialiazer)