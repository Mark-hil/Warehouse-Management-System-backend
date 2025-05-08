from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.utils import timezone
from .models import Customer, Sale, SaleItem, Payment, PriceHistory, Report
from .serializers import (
    CustomerSerializer, SaleSerializer, SaleItemSerializer,
    PaymentSerializer, PriceHistorySerializer, ReportSerializer
)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def purchase_history(self, request, pk=None):
        customer = self.get_object()
        sales = Sale.objects.filter(customer=customer)
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def sales_summary(self, request):
        today = timezone.now().date()
        sales_data = Sale.objects.filter(sale_date=today).aggregate(
            total_sales=Sum('total_amount'),
            total_orders=Count('sale_id')
        )
        return Response(sales_data)

    @action(detail=True, methods=['get'])
    def sale_items(self, request, pk=None):
        sale = self.get_object()
        items = SaleItem.objects.filter(sale=sale)
        serializer = SaleItemSerializer(items, many=True)
        return Response(serializer.data)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def payment_summary(self, request):
        today = timezone.now().date()
        payment_data = Payment.objects.filter(
            payment_date__date=today
        ).values('payment_method').annotate(
            total_amount=Sum('amount'),
            count=Count('payment_id')
        )
        return Response(payment_data)

class PriceHistoryViewSet(viewsets.ModelViewSet):
    queryset = PriceHistory.objects.all()
    serializer_class = PriceHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def current_prices(self, request):
        today = timezone.now().date()
        current_prices = PriceHistory.objects.filter(
            effective_from__lte=today,
            effective_to__isnull=True
        )
        serializer = self.get_serializer(current_prices, many=True)
        return Response(serializer.data)

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def generate_report(self, request):
        report_type = request.data.get('report_type')
        parameters = request.data.get('parameters', {})
        
        # Create a new report instance
        report = Report.objects.create(
            report_type=report_type,
            generated_by=request.user,
            parameters=parameters,
            result_data={},  # Will be updated after processing
            name=f"{report_type} Report - {timezone.now().strftime('%Y-%m-%d %H:%M')}"
        )
        
        # Process report based on type
        if report_type == 'SALES':
            result_data = self._process_sales_report(parameters)
        elif report_type == 'INVENTORY':
            result_data = self._process_inventory_report(parameters)
        else:
            return Response(
                {'error': 'Invalid report type'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update report with results
        report.result_data = result_data
        report.save()
        
        serializer = self.get_serializer(report)
        return Response(serializer.data)

    def _process_sales_report(self, parameters):
        # Implement sales report logic
        start_date = parameters.get('start_date')
        end_date = parameters.get('end_date')
        
        sales_data = Sale.objects.filter(
            sale_date__range=[start_date, end_date]
        ).aggregate(
            total_sales=Sum('total_amount'),
            total_orders=Count('sale_id')
        )
        
        return sales_data

    def _process_inventory_report(self, parameters):
        # Implement inventory report logic
        from inventory_management.models import Inventory
        
        warehouse_id = parameters.get('warehouse_id')
        category_id = parameters.get('category_id')
        
        query = Inventory.objects.all()
        if warehouse_id:
            query = query.filter(warehouse_id=warehouse_id)
            
        inventory_data = query.aggregate(
            total_items=Count('inventory_id'),
            total_quantity=Sum('available_quantity')
        )
        
        return inventory_data
