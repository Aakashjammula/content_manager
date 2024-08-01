FROM tensorflow:2.12.0-gpu

RUN apt-get update \
    && apt install -y git

RUN useradd -m tf
USER tf

RUN cd /home/tf \
    && git clone https://github.com/Aakashjammula/content_manager \
    && cd content_manager \
    && pip install -r reqs-without-tf.txt

WORKDIR /home/tf/content_manager
ENTRYPOINT python /home/tf/content_manager/main.py
