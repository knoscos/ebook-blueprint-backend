from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import openai
import requests

router = APIRouter()
openai.api_key = os.getenv("OPENAI_API_KEY")

class SectionRequest(BaseModel):
    title: str
    author: str
    section_name: str
    tone: str = "expert"

@router.post("/generate_section")
async def generate_section(req: SectionRequest):
    if not req.title or not req.author:
        raise HTTPException(status_code=400, detail="Title and author required.")
    
    prompt = (
        f"Write a professional, expert-guide style chapter titled '{req.section_name}' "
        f"for an ebook called '{req.title}' by {req.author}. "
        f"Include headings, steps, checklists, and a Pro Tip."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    text = response.choices[0].message["content"]

    img_query = req.section_name.replace(" ", "+")
    image_url = f"https://source.unsplash.com/1200x800/?{img_query}"

    return {
        "section_name": req.section_name,
        "text": text,
        "image_url": image_url
    }
