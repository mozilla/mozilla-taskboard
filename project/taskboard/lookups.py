from ajax_select import LookupChannel
from django.utils.html import escape
from django.db.models import Q
from users.models import UserProfile

class UserProfileLookup(LookupChannel):

    model = UserProfile

    def get_query(self, q, request):
        return UserProfile.objects.filter(Q(display_name__icontains=q) | Q(user__email__istartswith=q)).order_by('display_name')

    def check_auth(self, request):
        return request.user.userprofile.is_vouched

    def get_result(self,obj):
        """Text repr of result."""
        return obj.display_name

    def format_match(self,obj):
        """HTML formatted item for display in the dropdown"""
        return self.format_item_display(obj)

    def format_item_display(self,obj):
        """HTML formatted item for displaying item in the selected deck area"""
        return u"%s<div><i>%s</i></div>" % (escape(obj.display_name),escape(obj.user.email))

