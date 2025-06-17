from import_export import resources, fields
from .models import *
import json
from import_export.widgets import DateWidget, TimeWidget

class Time_table_Resource(resources.ModelResource):
    date = fields.Field(
        column_name='date',
        attribute='date',
        widget=DateWidget(format='%d-%m-%Y')
    )

    start_time = fields.Field(
        column_name='start_time',
        attribute='start_time',
        widget=TimeWidget(format='%H:%M')
    )

    end_time = fields.Field(
        column_name='end_time',
        attribute='end_time',
        widget=TimeWidget(format='%H:%M'))

    class Meta:
        model = Time_table
        exclude = ('id', 'day')
        import_id_fields = ['class_name', 'subject_teacher', 'class_no', 'class_room_no', 'start_time', 'end_time', 'date']
        fields = ('class_name', 'subject_teacher', 'class_no', 'class_room_no', 'start_time', 'end_time', 'date')
        export_order = ('class_name', 'subject_teacher', 'class_no', 'class_room_no', 'start_time', 'end_time', 'date')

    def import_data(self, dataset, dry_run = False, raise_errors=True, use_transactinos=None, **kwargs):
        from import_export.results import Result
        result = Result()

        if dry_run:
            return super().import_data(dataset, dry_run, raise_errors, use_transactinos, **kwargs)
        
        time_table = []
        for row in dataset.dict:
            try:
                time_table.append(Time_table(
                    class_name = row["class_name"],
                    subject_teacher = row["subject_teacher"],
                    class_no = row["class_no"],
                    class_room_no = row["class_room_no"],
                    start_time = row["start_time"],
                    end_time = row["end_time"],
                    date = row["date"],
                    day=row["date"].strftime("%A")
                ))
            except Exception as e:
                result.invalid_rows.append((row, str(e)))
            
        if not dry_run:
            Time_table.objects.bulk_create(time_table, batch_size=100000)

        result.totals['new'] = len(time_table)
        return result