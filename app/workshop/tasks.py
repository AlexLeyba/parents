from celery import shared_task


@shared_task(name="tasks.to_publish_task")
def to_publish_task(day_id):
    from .models import Day

    day = Day.objects.get(id=day_id)
    day.publish = True
    day.save()
    return True
