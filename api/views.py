from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum, Avg

# Import models from their new locations
from inventory_management.models import (
    Item as ProductDim,
    Category as CategoryDim,
    Inventory as InventoryAndPriceFact
)
from user_accounts.models import User as CustomerDim
from procurement_system.models import (
    Supplier as SupplierDim,
    Purchase as SalesFact
)
from shipment_tracking.models import (
    ShipmentTracking as ShippingDim,
    Return as PaymentDim
)
from dimensions.models import (
    DateDim,
    StoreDim,
    PromotionDim
)
from .serializers import (
    InventoryAndPriceFactSerializer,
    ProductDimSerializer,
    DateDimSerializer,
    StoreDimSerializer,
    SupplierDimSerializer,
    CategoryDimSerializer,
    SalesFactSerializer,
    CustomerDimSerializer,
    PromotionDimSerializer,
    ShippingDimSerializer,
    PaymentDimSerializer
)

class InventoryAndPriceFactViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryAndPriceFact.objects.all()
    serializer_class = InventoryAndPriceFactSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def product_inventory(self, request):
        product_key = request.query_params.get('product_key')
        if product_key:
            inventory = InventoryAndPriceFact.objects.filter(product_key=product_key)
            serializer = self.get_serializer(inventory, many=True)
            return Response(serializer.data)
        return Response({'error': 'product_key parameter is required'}, status=400)

class ProductDimViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductDim.objects.all()
    serializer_class = ProductDimSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def by_category(self, request):
        category_key = request.query_params.get('category_key')
        if category_key:
            products = ProductDim.objects.filter(category_key=category_key)
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        return Response({'error': 'category_key parameter is required'}, status=400)

class DateDimViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DateDim.objects.all()
    serializer_class = DateDimSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def by_year(self, request):
        year = request.query_params.get('year')
        if year:
            dates = DateDim.objects.filter(year=year)
            serializer = self.get_serializer(dates, many=True)
            return Response(serializer.data)
        return Response({'error': 'year parameter is required'}, status=400)

class StoreDimViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StoreDim.objects.all()
    serializer_class = StoreDimSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def by_state(self, request):
        state = request.query_params.get('state')
        if state:
            stores = StoreDim.objects.filter(state=state)
            serializer = self.get_serializer(stores, many=True)
            return Response(serializer.data)
        return Response({'error': 'state parameter is required'}, status=400)

    @action(detail=False, methods=['GET'])
    def by_city(self, request):
        city = request.query_params.get('city', None)
        if city:
            stores = StoreDim.objects.filter(city=city)
            serializer = self.get_serializer(stores, many=True)
            return Response(serializer.data)
        return Response({'error': 'city parameter is required'}, status=400)

class SupplierDimViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SupplierDim.objects.all()
    serializer_class = SupplierDimSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def by_country(self, request):
        country = request.query_params.get('country', None)
        if country:
            suppliers = SupplierDim.objects.filter(country=country)
            serializer = self.get_serializer(suppliers, many=True)
            return Response(serializer.data)
        return Response({'error': 'country parameter is required'}, status=400)

class CategoryDimViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CategoryDim.objects.all()
    serializer_class = CategoryDimSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def by_department(self, request):
        department = request.query_params.get('department', None)
        if department:
            categories = CategoryDim.objects.filter(department=department)
            serializer = self.get_serializer(categories, many=True)
            return Response(serializer.data)
        return Response({'error': 'department parameter is required'}, status=400)

class SalesFactViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SalesFact.objects.all()
    serializer_class = SalesFactSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def sales_by_product(self, request):
        product_key = request.query_params.get('product_key')
        if product_key:
            sales = SalesFact.objects.filter(product_key=product_key)
            total_sales = sales.aggregate(
                total_quantity=Sum('quantity'),
                total_revenue=Sum('net_price'),
                total_profit=Sum('profit'),
                avg_discount=Avg('discount_amount')
            )
            return Response(total_sales)
        return Response({'error': 'product_key parameter is required'}, status=400)

    @action(detail=False, methods=['GET'])
    def sales_by_store(self, request):
        store_key = request.query_params.get('store_key')
        if store_key:
            sales = SalesFact.objects.filter(store_key=store_key)
            total_sales = sales.aggregate(
                total_quantity=Sum('quantity'),
                total_revenue=Sum('net_price'),
                total_profit=Sum('profit')
            )
            return Response(total_sales)
        return Response({'error': 'store_key parameter is required'}, status=400)

    @action(detail=False, methods=['GET'])
    def customer_sales(self, request):
        customer_key = request.query_params.get('customer_key')
        if customer_key:
            sales = SalesFact.objects.filter(customer_key=customer_key)
            total_sales = sales.aggregate(
                total_purchases=Sum('quantity'),
                total_spent=Sum('net_price'),
                total_savings=Sum('discount_amount'),
                total_profit=Sum('profit')
            )
            return Response(total_sales)
        return Response({'error': 'customer_key parameter is required'}, status=400)

class CustomerDimViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomerDim.objects.all()
    serializer_class = CustomerDimSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def by_status(self, request):
        status = request.query_params.get('status', None)
        if status:
            customers = CustomerDim.objects.filter(status=status)
            serializer = self.get_serializer(customers, many=True)
            return Response(serializer.data)
        return Response({'error': 'status parameter is required'}, status=400)

class PromotionDimViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PromotionDim.objects.all()
    serializer_class = PromotionDimSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def active(self, request):
        from django.utils import timezone
        today = timezone.now().date()
        promotions = PromotionDim.objects.filter(start_date__lte=today, end_date__gte=today)
        serializer = self.get_serializer(promotions, many=True)
        return Response(serializer.data)

class ShippingDimViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ShippingDim.objects.all()
    serializer_class = ShippingDimSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def by_carrier(self, request):
        carrier = request.query_params.get('carrier', None)
        if carrier:
            shipping = ShippingDim.objects.filter(carrier=carrier)
            serializer = self.get_serializer(shipping, many=True)
            return Response(serializer.data)
        return Response({'error': 'carrier parameter is required'}, status=400)

class PaymentDimViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentDim.objects.all()
    serializer_class = PaymentDimSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def by_payment_type(self, request):
        payment_type = request.query_params.get('payment_type', None)
        if payment_type:
            payments = PaymentDim.objects.filter(payment_type=payment_type)
            serializer = self.get_serializer(payments, many=True)
            return Response(serializer.data)
        return Response({'error': 'payment_type parameter is required'}, status=400)
