from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import InvoiceSerializer, UserSerializer, ProviderSerializer
from rest_framework.permissions import AllowAny
from .models import Invoice, Provider
from .permissions import IsPlacerUser, IsApproverUser
from .models import Item


class ProviderViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()
    permission_classes = [IsAuthenticated, IsPlacerUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()

    def get_permissions(self):
        if self.action in ["create"]:
            return [IsAuthenticated(), IsPlacerUser()]
        elif self.action in ["update_state"]:
            return [IsAuthenticated(), IsApproverUser()]
        elif self.action in ["update_items"]:
            return [IsPlacerUser(), IsAuthenticated()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=True,
        methods=["patch"],
        url_path="items",
    )
    def update_items(self, request, pk=None):
        invoice = self.get_object()
        items_data = request.data.get("items", [])

        invoice.items.all().delete()

        for item_data in items_data:
            Item.objects.create(
                invoice=invoice,
                name=item_data["name"],
                quantity=item_data["quantity"],
                price=item_data["price"],
            )

        invoice.save()
        serializer = self.get_serializer(invoice)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], url_path="state",)
    def update_state(self, request, pk=None):
        invoice = self.get_object()

        if "state" not in request.data:
            return Response(
                {"error": "State is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        new_state = request.data.get("state")

        if new_state not in [s[0] for s in Invoice.State.choices]:
            return Response(
                {"error": "Invalid state"}, status=status.HTTP_400_BAD_REQUEST
            )

        invoice.state = new_state
        invoice.save()
        return Response(InvoiceSerializer(invoice).data)


# class ItemViewSet(viewsets.ModelViewSet):
#     serializer_class = ItemSerializer
#     queryset = Item.objects.all()
#     permission_classes = [IsAuthenticated, IsPlacerUser]

#     def perform_create(self, serializer):
#         invoice_id = self.request.data.get("invoice")
#         invoice = get_object_or_404(Invoice, id=invoice_id)
#         serializer.save(invoice=invoice)


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        return [AllowAny()]
        # if self.action == "create":
        #     return [AllowAny()]
        # return super().get_permissions()
