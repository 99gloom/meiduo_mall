# celery -A celery_tasks.main  worker --concurrency=4 --loglevel=INFO -P threads -n worker%n