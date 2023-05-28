import logging
from django.shortcuts import render

import whisper_timestamped as whisper

from stt.video_transcription import run_transcription, model

logger = logging.getLogger(__name__)


def upload_file(request):

    if request.method == 'POST':
        file = request.FILES['file']
        # save file locally to media folder
        file_path = f'media/{file.name}'
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        transcription_text = run_transcription(file_path, model)

        return render(request, 'output_page.html', {'output_text': transcription_text})

    return render(request, 'upload_file.html')