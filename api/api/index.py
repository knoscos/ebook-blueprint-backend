from fastapi import FastAPI
from api.generate_section import router as generate_router
from api.compile_pdf import router as pdf_router

app = FastAPI()

# include your routes
app.include_router(generate_router)
app.include_router(pdf_router)

# Vercel looks for a variable called "app"
# DO NOT rename it.
