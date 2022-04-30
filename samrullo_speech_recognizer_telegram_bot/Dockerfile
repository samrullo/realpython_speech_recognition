FROM python:3
WORKDIR /usr/src/app
COPY ./requirements.in ./
RUN apt-get update
RUN apt-get --yes install portaudio19-dev
RUN apt-get --yes install ffmpeg
RUN pip install pip-tools
RUN pip-compile
RUN pip-sync

COPY . .
CMD ["python","speech_recognition_bot.py"]