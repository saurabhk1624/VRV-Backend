from rest_framework import serializers

from common.models import Dropdown, LeftPanel


class DropdownSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Dropdown
        fields = ["id", "field", "children"]

    def get_children(self, obj):
        children = Dropdown.objects.filter(parent=obj)
        if children.exists():
            return DropdownSerializer(children, many=True, context=self.context).data
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not representation.get("children"):
            representation.pop("children")
        return representation


class LeftPanelSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = LeftPanel
        fields = ["id", "icon", "field", "route", "priority", "children"]

    def get_children(self, obj):
        children = LeftPanel.objects.filter(parent=obj, status=True).order_by(
            "priority"
        )
        return LeftPanelSerializer(children, many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not representation.get("children"):
            representation.pop("children")
        return representation
