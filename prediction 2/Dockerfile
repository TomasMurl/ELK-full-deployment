FROM bitnami/pytorch:2

EXPOSE 80/tcp

# RUN apt-get update \
# && apt-get -y install --no-install-recommends ffmpeg libsm6 libxext6 \
# && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt 
WORKDIR /home/
COPY predict.py /home/predict.py
COPY CustomModel.py /home/CustomModel.py
USER root
RUN python3 -c "from transformers import DistilBertTokenizerFast; DistilBertTokenizerFast.from_pretrained('distilbert-base-cased')"
ENTRYPOINT ["python", "-m", "aiohttp.web", "-H", "0.0.0.0", "-P", "80", "predict:init_func"]