import django_filters
from drf_yasg import renderers
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from company.models import Company, Item
from company.serializers import CompanySerializer, ItemSerializer
from finance.models import Cart
from users.permissions import IsOwner, IsActive, IsUser

from django.forms.models import model_to_dict


class CompanyViewSet(ModelViewSet):

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsOwner,)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['city', 'country']

    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

        company = serializer.save()

        items = company.item.all()

        for item in items:
            data = model_to_dict(item, exclude=['id', 'owner'])
            if not Item.objects.filter(**data, owner=self.request.user).exists():
                Item.objects.create(**data, owner=self.request.user)

    def perform_update(self, serializer, pk=None):

        company = serializer.save()

        items = company.item.all()

        for item in items:
            data = model_to_dict(item, exclude=['id', 'owner'])
            if not Item.objects.filter(**data, owner=self.request.user).exists():
                Item.objects.create(**data, owner=self.request.user)

        cart = Cart.objects.filter(owner=self.request.user).first()
        company.balance -= cart.total
        company.save()


class ItemViewSet(ModelViewSet):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsActive, IsUser)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
