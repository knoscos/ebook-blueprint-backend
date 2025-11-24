from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import FileResponse
import tempfile
import requests
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

router = APIRouter()

class CompileRequest(BaseModel):
    title: str
    author: str
    sections: list[dict]  # each item: {"section_name":..., "text":..., "image_url":...}

@router.post("/compile_pdf")
async def compile_pdf(req: CompileRequest):

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(tmp.name, pagesize=A4)
    width, height = A4
    margin = 2 * cm

    # ---- COVER PAGE ----
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(width / 2, height / 2 + 2 * cm, req.title)
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2, height / 2 - 0.5 * cm, f"by {req.author}")
    c.showPage()

    # ---- TABLE OF CONTENTS ----
    c.setFont("Helvetica-Bold", 24)
    c.drawString(margin, height - margin, "Table of Contents")
    y = height - margin * 2

    c.setFont("Helvetica", 14)
    for i, s in enumerate(req.sections, 1):
        c.drawString(margin, y, f"{i}. {s['section_name']}")
        y -= 0.8 * cm
        if y < margin:
            c.showPage()
            y = height - margin * 2
    c.showPage()

    # ---- SECTIONS ----
    for section in req.sections:
        # Section Title
        c.setFont("Helvetica-Bold", 22)
        c.drawString(margin, height - margin, section["section_name"])
        y = height - margin * 2

        # Section Image
        try:
            img_path = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
            r = requests.get(section["image_url"], timeout=10)
            with open(img_path, "wb") as f:
                f.write(r.content)
            c.drawImage(img_path, margin, y - 10 * cm, width - 2 * margin, 9 * cm, preserveAspectRatio=True)
            y -= 11 * cm
        except:
            pass

        # Section Text
        c.setFont("Helvetica", 12)
        for line in section["text"].split("\n"):
            if y < margin * 2:
                c.showPage()
                y = height - margin * 2
            c.drawString(margin, y, line[:120])
            y -= 0.5 * cm

        c.showPage()

    c.save()

    return FileResponse(
        tmp.name,
        filename=f"{req.title}.pdf",
        media_type="application/pdf"
    )
