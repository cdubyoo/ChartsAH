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
    date_traded = django_filters.DateTimeFilter(field_name='date_traded', label ="Exact Date",
        widget=forms.DateInput(attrs={'class': 'datepicker'}))
  
    # --enable if want to do date range instead--  gte =  greater than or equal to
    start_date = DateFilter(field_name="date_traded", lookup_expr='gte', label="Date Min",
    widget=forms.DateInput(attrs={'class': 'datepicker'})) 
    end_date = DateFilter(field_name="date_traded", lookup_expr='lte',label="Date Max",
    widget=forms.DateInput(attrs={'class': 'datepicker'}))  
    class Meta:

        model = Post
        fields = []

    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        # at startup if no data, then empty query set
        if self.data == {}:
            self.queryset = self.queryset.none()