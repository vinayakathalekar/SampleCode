from fastapi import FastAPI
import gradio as gr
from pydantic import BaseModel
from rule_engine import run_rules, Claim
import json

#############################################
# Install following PIP packages:           #
# 1. pip install FastAPI                    #
# 2. pip install uvicorn                    #
# 3. pip install gradio                     #
# 4. pip install pydantic                   #
# 5. pip install business_rules             #
# Run the app by running: uvicorn main:app  #
#############################################


class Request(BaseModel):
    claimantName: str
    treatmentType: str
    treatment: str


class Response(BaseModel):
    message: str


app = FastAPI()


@app.get('/')
async def read_main():
    return {"message": "This is your main app"}


@app.post('/check_qualification', response_model=Response)
async def calculate(request: Request):
    print(request)
    return qualification(request)


def qualification(request: Request):
    print('body ::', request)
    _claim = Claim(request.claimantName, request.treatmentType,
                   request.treatment)
    print('Received Claim input ::', _claim.treatment)
    # call rule engine passing claim received
    result = run_rules(_claim)
    print('Results from Rule accepted, rejected, verify :: ', 
          result.accepted, result.rejected, result.verify)
    if result.accepted is True:
        return Response(message='Given treatment is accepted as per guidelines')
    elif result.rejected is True:
        return Response(message='Given treatment is rejected as per guidelines')
    elif result.verify is True:
        return Response(message='Given treatment is sent to verification')
    else:
        return Response(message='No rule matched')

def call_api(claimantName, treatmentType, treatment):
    request = Request(
        claimantName=claimantName,
        treatmentType=treatmentType,
        treatment=treatment
    )
    result = f'Result: {qualification(request).message}'
    return result


io = gr.Interface(
    fn=call_api,
    inputs=[
        gr.Textbox(label="Claimant Name"),
        gr.Textbox(label="Treatment Type"),
        gr.Textbox(label="Treatment Performed"),
        # "text",
        # "text",
        # gr.Textbox(lines=5, placeholder="Put in your list here ..."),
        # "checkbox",
        # gr.Slider(0, 100)
    ],
    outputs=[gr.Textbox(lines=5)],
    title="Claim Adjudication",
    description="",
)

app = gr.mount_gradio_app(app, io, path='/demo')
