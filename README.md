# Ebook Blueprint Backend

A FastAPI-powered backend for generating premium, professionally-formatted ebooks with:
- Chapter generation using OpenAI
- Automatic image selection
- PDF compilation with cover page, TOC, and styled sections

## Endpoints

### `POST /generate_section`
Generates text + image for a single chapter.

### `POST /compile_pdf`
Takes all chapters and returns a downloadable PDF.

## Environment Variables
Set this in Vercel:


## Deployment
Automatically deployed on Vercel using `vercel.json`.
