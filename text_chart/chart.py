import openai
from fastapi import Request, HTTPException, APIRouter

router = APIRouter()

# Configure OpenAI
openai.api_key = "your_openai_api_key"
model = "code-davinci-edit-001"


# Define the route for generating the pie chart
@router.post('/generate_pie_chart')
async def generate_pie_chart(instruction: str):
    try:
        response = openai.Edit.create(
            model=model,
            instruction=instruction,
            temperature=0,
            top_p=1
        )

        generated_text = response['choices'][0]['text']
        return {"result": generated_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
