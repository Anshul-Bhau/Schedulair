from import_export import resources, fields
from .models import *

class Time_table_Resource(resources.ModelResource):
    class Meta:
        model = Time_table
        exclude = ('id',)
        import_id_fields = ["day", 'class_name', 'subject_teacher', 'class_no', 'class_room_no', 'start_time', 'end_time', 'date']
        fields = ('phase', 'class_name', 'date', 'start_time', 'end_time', 'venue', 'total_students', 'ins_email', 'ins_name', 'batch_id', 'batch_name')
        export_order = ('phase', 'class_name', 'date', 'start_time', 'end_time', 'venue', 'total_students', 'ins_email', 'ins_name', 'batch_id', 'batch_name')
