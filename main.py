from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from uuid import uuid4
from typing import Annotated, Union
from fastapi import Form
import plotly.graph_objects as go

from fastapi import FastAPI, Header, Request, Form
import os
from openlayer import Openlayer

client = Openlayer(
    api_key=os.environ.get("OPENLAYER_API_KEY"),  # This is the default and can be omitted
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/mapview", response_class=HTMLResponse)
async def mapview(request: Request):
    # Example usage of Openlayer to perform some backend inference
    response = client.inference_pipelines.data.stream(
        inference_pipeline_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        config={
            "input_variable_names": ["user_query"],
            "output_column_name": "output",
            "num_of_token_column_name": "tokens",
            "cost_column_name": "cost",
            "timestamp_column_name": "timestamp",
        },
        rows=[
            {"user_query": "Map data processing query"}
        ],
    )
    
    # Process Openlayer response
    success = response.success
    output = response.results[0]["output"] if success else "No output from pipeline"

    return templates.TemplateResponse(
        "map.html", {"request": request, "openlayer_output": output}
    )
