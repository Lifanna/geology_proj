from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.viewsets import ViewSet
from main.api import serializers
from main import models
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.core.files.uploadedfile import InMemoryUploadedFile
from main.api import image_decoder
import io


class WaterCourseChildrenDetailView(ListAPIView):
    serializer_class = serializers.WaterCourseChildrenSerializer
    model = serializer_class.Meta.model
    paginate_by = 100

    def get_queryset(self):
        parent = self.kwargs['pk']
        queryset = self.model.objects.filter(parent_watercourse_id=parent)

        return queryset.order_by('-id')


class TaskListView(ListAPIView):
    serializer_class = serializers.TaskSerializer
    model = serializer_class.Meta.model
    permission_classes = [IsAuthenticated,]

    def list(self, request):
        print("DDDD:", request.user.id)
        queryset = self.serializer_class.Meta.model.objects.filter(responsible__id=request.user.id, status__name="на выполнении").all()

        serializer = serializers.TaskSerializer(queryset, many=True)

        return Response(serializer.data)


class LayerCreateAPIView(CreateAPIView, ListAPIView):
    queryset = models.Layer.objects.all()
    serializer_class = serializers.LayerSerializer
    # permission_classes = [IsAuthenticated,]


class WellCreateAPIView(CreateAPIView, ListAPIView):
    queryset = models.Well.objects.all()
    serializer_class = serializers.WellSerializer
    # permission_classes = [IsAuthenticated,]


class LayerMaterialsListAPIView(ListAPIView):
    serializer_class = serializers.LayerMaterialSerializer
    model = serializer_class.Meta.model
    permission_classes = [IsAuthenticated,]

    def list(self, request):
        queryset = self.serializer_class.Meta.model.objects.all()

        serializer = serializers.LayerMaterialSerializer(queryset, many=True)

        return Response(serializer.data)


class SyncronizeViewSet(ViewSet):
    def create(self, request):
        success = False
        post_data = request.data

        print("EEEEEEE: ", post_data.get('tasks'))

        for task in post_data.get('tasks'):
            existing_task = models.Task.objects.get(pk=task.get('id'))
            existing_task.status = models.TaskStatus.objects.get(name=task.get('status_name'))

            existing_task.save()

        for well in post_data.get('wells'):
            well_object, well_exists = models.Well.objects.get_or_create(name=well.get('name'))
            well_object.description = well.get('description')
            well_object.comment = well.get('comment')
            well_object.line = models.Line.objects.get(pk=well.get('line_id'))
            # well_object.created_at = well.get('created_at')
            # well_object.updated_at = well.get('updated_at')

            img = image_decoder.decode_design_image(well.get('pillar_photo_file'))
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG')
            photo_unique_name = well.get('name') + "_" + str(well.get('line_id'))
            well_object.pillar_photo = InMemoryUploadedFile(img_io, field_name=None, name=photo_unique_name + ".jpg", content_type='image/jpeg', size=img_io.tell, charset=None)

            well_object.save()

        for layer in post_data.get('layers'):
            # print("TTTTTTTTTT:", layer.get('layer_material_id'))
            layer_well = models.Well.objects.get(name=layer.get('well_name'), line__id=layer.get('line_id'))
            layer_layer_material = models.LayerMaterial.objects.get(pk=layer.get('layer_material_id'))
            layer_object, layer_exists = models.Layer.objects.get_or_create(
                name=layer.get('name'), well=layer_well, layer_material=layer_layer_material
            )
            layer_object.well = layer_well
            # layer_object.responsible = request.user
            layer_object.responsible = models.CustomUser.objects.get(pk=1)
            layer_object.name = layer.get('name')
            layer_object.description = layer.get('description')
            layer_object.comment = layer.get('comment')
            layer_object.layer_material = layer_layer_material
            layer_object.sample_obtained = layer.get('sample_obtained')
            layer_object.drilling_stopped = layer.get('drilling_stopped')
            layer_object.aquifer = layer.get('aquifer')
            # layer_object.created_at = layer.get('created_at')
            # layer_object.updated_at = layer.get('updated_at')

            layer_object.save()

        for well_task in post_data.get('wellTasks'):
            well_task_well = models.Well.objects.get(name=well_task.get('well_name'), line__id=well_task.get('line_id'))
            well_task_task = models.Task.objects.get(pk=well_task.get('task_id'))
            well_task, well_task_exists = models.WellTask.objects.get_or_create(
                well=well_task_well, task=well_task_task
            )
            well_task.well = well_task_well
            well_task.task = well_task_task

            well_task.save()
            success = True

        return Response(data={"status": success})


class LineListAPIView(ListAPIView):
    serializer_class = serializers.LineSerializer
    model = serializer_class.Meta.model
    permission_classes = [AllowAny,]

    def list(self, request, watercourse_id):
        queryset = self.serializer_class.Meta.model.objects.filter(watercourse__id=watercourse_id).all()

        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)
