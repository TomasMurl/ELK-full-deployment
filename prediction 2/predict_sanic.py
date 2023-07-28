import os
from sanic import Sanic
from sanic.response import json, empty
from CustomModel import Model
from elasticsearch import Elasticsearch as es


def strip_event(json_obj):
	temp_data = str(json_obj["message"])
	temp_data = temp_data.replace("\t"," ").replace("\n","")
	return(temp_data)

#init
# model_path = os.environ["model_path"]
model_path = "C:\\Users\\Tomas\\Desktop\\models_host\\models\\distilbert-base-cased-finetuned-conll03-english"
model = Model(model_path, "distilbert-base-cased")
app = Sanic("predictapi")
elk = es("http://localhost:9200", http_auth=("elastic", "JxkKadntsxrl39HBaLaZ"))

#api routes
@app.post("/predict")
async def prediction(request):
	raw_json = request.json
	data = strip_event(raw_json)
	answer   = model.predict(data)
	raw_json["ML answer"] = answer
	elk.index(index="my_index", document=raw_json)
	return empty()

@app.get("/")
async def index(request):
	return json({"state":"alive"})