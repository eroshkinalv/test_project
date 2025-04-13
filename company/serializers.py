from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from company.models import Item, Company


class ItemSerializer(ModelSerializer):

    class Meta:
        model = Item
        fields = "__all__"


class CompanySerializer(ModelSerializer):

    def validate(self, attrs):

        company_type = attrs.get("company_type")
        supplier = attrs.get("supplier")
        items = attrs.get("item")

        if company_type != "Завод":
            if not supplier:
                raise ValidationError("Выберите поставщика.")

            for item in items:

                if item not in supplier.item.all():
                    raise ValidationError("Выберите товар Вашего поставщика.")

        return attrs

    supplier_info = SerializerMethodField()

    def get_supplier_info(self, company):

        if company.supplier:
            supplier_id = company.supplier.id
            supplier_info = Company.objects.filter(id=supplier_id)
            serializer = CompanySerializer(supplier_info, many=True)
            return serializer.data

    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ["owner", "balance", "created_at"]
