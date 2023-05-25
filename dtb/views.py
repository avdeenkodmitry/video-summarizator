import json
import logging
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from telegram import Update

from dtb.celery import app
from dtb.settings import DEBUG
from tgbot.dispatcher import dispatcher
from tgbot.main import bot

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def process_telegram_event(update_json):
    update = Update.de_json(update_json, bot)
    dispatcher.process_update(update)


def index(request):
    return JsonResponse({"error": "sup hacker"})


class TelegramBotWebhookView(View):
    # WARNING: if fail - Telegram webhook will be delivered again.
    # Can be fixed with async celery task execution
    def post(self, request, *args, **kwargs):
        if DEBUG:
            process_telegram_event(json.loads(request.body))
        else:
            # Process Telegram event in Celery worker (async)
            # Don't forget to run it and & Redis (message broker for Celery)!
            # Locally, You can run all of these services via docker-compose.yml
            process_telegram_event.delay(json.loads(request.body))

        # e.g. remove buttons, typing event
        return JsonResponse({"ok": "POST request processed"})

    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request received! But nothing done"})


@app.task(ignore_result=True)
def send_video_to_nn(file_name, **params):
    update = Update.de_json(update_json, bot)

    dispatcher.process_update(update)
    return None

def upload_file(request):
    #
    if request.method == 'POST':
        file = request.FILES['file']
        # save file locally to media folder
        with open(f'media/{file.name}_{}', 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        send_video_to_nn.delay(file.name)

        return render(request, 'upload_success.html', {'filename': file.name})

    return render(request, 'upload_file.html')
