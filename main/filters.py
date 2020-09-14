import django_filters
from django_filters import DateFilter
from django import forms
from taggit.forms import TagField
from .models import Post

# to enable taggit tags to be used in django-filters
class TagFilter(django_filters.CharFilter):
    field_class = TagField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('lookup_expr', 'in')
        super().__init__(*args, **kwargs)



class PostFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='user__username', label='User')
    ticker = django_filters.CharFilter()
    tags = TagFilter(field_name='tags__name', label='Tags', help_text=('Press Enter or comma to seperate tags.'), distinct=True,  
        widget=forms.TextInput(attrs={'data-role':'tagsinput'}))
    date_traded = django_filters.DateTimeFilter(field_name='date_traded', 
        widget=forms.DateInput(attrs={'class': 'datepicker'}))
  
    # --enable if want to do date range instead--
    #start_date = DateFilter(field_name="date_traded", lookup_expr='gte') #gte =  greater than or equal to
    #end_date = DateFilter(field_name="date_traded", lookup_expr='lte') 
    class Meta:

        model = Post
        fields = []