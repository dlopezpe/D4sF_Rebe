from .models import Enterprise
from rest_framework import serializers
from django.core.paginator import Paginator
from django.db.models import Sum

from ..parcelas.serializer import ParcelSerializerArea


class EnterpriseSerializer(serializers.ModelSerializer):
    parcels = serializers.SerializerMethodField('paginated_parcels')
    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'direction', 'phone_number', 'cif', 'hectares_available', 'is_active', 'sentinel_instance', 'parcels','type_metric', 'cooperative','continent','is_monitor')
        
    #parcels = ParcelSerializerArea(many=True, required=False)
    def paginated_parcels(self, obj):
        search_param = self.context['request'].query_params.get('parcel_mame') or ''
        page_size = self.context['request'].query_params.get('size') or 99999999
        colum_name = self.context['request'].query_params.get('colum_name') or ''
        order = self.context['request'].query_params.get('order') or ''
        """
        if search_param:
            paginator = Paginator(obj.parcels.filter(name__icontains=search_param), page_size)
        else:
            paginator = Paginator(obj.parcels.all(), page_size)
        """
        
        if colum_name:
            if order == 'descending':
                if search_param:
                    paginator = Paginator(obj.parcels.filter(name__icontains=search_param).order_by('-'+colum_name), page_size)
                else:
                    paginator = Paginator(obj.parcels.all().order_by('-'+colum_name), page_size)
            elif order == "ascending":
                if search_param:
                    paginator = Paginator(obj.parcels.filter(name__icontains=search_param).order_by(colum_name), page_size)
                else:
                    paginator = Paginator(obj.parcels.all().order_by(colum_name), page_size)
            else:
                if search_param:
                    paginator = Paginator(obj.parcels.filter(name__icontains=search_param), page_size)
                else:
                    paginator = Paginator(obj.parcels.all().order_by('name'), page_size)
        else:
            if search_param:
                paginator = Paginator(obj.parcels.filter(name__icontains=search_param).order_by('name'), page_size)
            else:
                paginator = Paginator(obj.parcels.all().order_by('name'), page_size)

        page = self.context['request'].query_params.get('page') or 1
        words_in_book = paginator.page(page)
        serializer = ParcelSerializerArea(words_in_book, many=True, required=False)
        return serializer.data

class EnterpriseSerializerCount(serializers.ModelSerializer):
    parcels = serializers.SerializerMethodField('count_parcels')
    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'direction', 'phone_number', 'cif', 'hectares_available', 'is_active', 'sentinel_instance', 'parcels', 'type_metric','continent','is_monitor')
    
    def count_parcels(self, obj):
        count = obj.parcels.count()
        return count


class EnterpriseSerializerExcept(serializers.ModelSerializer):
    parcels = serializers.SerializerMethodField('except_parcel')
    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'direction', 'phone_number', 'cif', 'hectares_available', 'is_active', 'sentinel_instance', 'parcels', 'type_metric','continent','is_monitor')
    
    def except_parcel(self, obj):
        parcel_ex = self.context['request'].query_params.get('parcel') or ''
        area = obj.parcels.all().exclude(id=parcel_ex).aggregate(Sum('area'))
        return area