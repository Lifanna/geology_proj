from rest_framework.generics import ListAPIView
from main.api import serializers

class WaterCourseChildrenDetailView(ListAPIView):
    serializer_class = serializers.WaterCourseChildrenSerializer
    model = serializer_class.Meta.model
    paginate_by = 100

    def get_queryset(self):
        parent = self.kwargs['pk']
        queryset = self.model.objects.filter(parent_watercourse_id=parent)

        return queryset.order_by('-id')
