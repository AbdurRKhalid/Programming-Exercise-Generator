from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, HTTPException
import requests
import openai

api_key = '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'
openai.api_key = api_key

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def root(request: Request):
    data = await request.json()
    line = data.get("line")
    language = data.get("language")

    if not line or not language:
        raise HTTPException(status_code=422, detail="Both 'line' and 'language' parameters are required.")

    try:
        response = openai.Completion.create(
            engine="text-curie-001",
            prompt=line,
            max_tokens=500
        )
        message = response.choices[0].text.strip()

        generate_code = openai.Completion.create(
            engine="text-davinci-002",
            prompt="Write code for the " + message + f" in {language} programming language.",
            max_tokens=1000
        )
        code = generate_code.choices[0].text.strip()

        deepai_data = "Write code for the " + message + f" in {language} programming language."

        r = requests.post(
            "https://api.deepai.org/api/text-generator",
            data={
                'text': deepai_data,
            },
            headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
        )
        response_json = r.json()
        output_text = response_json['output']

        return {"response": message, "code": code, "deepai": output_text }

    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI Error: {e}")

