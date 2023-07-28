import asyncio
from aiohttp import web
from CustomModel import Model
from elasticsearch import Elasticsearch as es
import os

def init_func(argv):
    app = web.Application()
    app.router.add_post('/predict', predict)
    app.router.add_get('/', index)

    # model_path   = "C:\\Users\\Tomas\\Desktop\\models_host\\models\\distilbert-base-cased-finetuned-conll03-english"
    model_path   = os.environ["model_path"]

    app["model"] = Model(model_path, "distilbert-base-cased")
    app["elk"]   = es(
        "https://192.168.56.1:9200",
        use_ssl=True,
        verify_certs=False,
        ca_certs='D:\\elasticsearch\\ca.crt',
        http_auth=("elastic", "JxkKadntsxrl39HBaLaZ")
    )

    return app

def strip_event(json_obj):
    temp_data = str(json_obj["message"])
    temp_data = temp_data.replace("\t"," ").replace("\n","")
    return(temp_data)

async def index(request):
    return web.json_response({"state":"alive"}, status=200)

async def predict(request):
    try:
        raw_json = await request.json()
        data     = strip_event(raw_json)
        answer   = request.app["model"].predict(data)

        raw_json["ML answer"] = answer

        request.app["elk"].index(index="my_index", document=raw_json)

        return web.json_response({"state":"alive"}, status=200)

    except Exception as e:
        return web.json_response({'error': 'An error occurred while processing the request.'}, status=500)

