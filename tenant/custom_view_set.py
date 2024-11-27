from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin
from rest_framework.viewsets import GenericViewSet


class CustomViewSet(GenericViewSet, CreateModelMixin,
                    ListModelMixin,
                    UpdateModelMixin,
                    RetrieveModelMixin,
                    DestroyModelMixin):
    pass
