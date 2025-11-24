# utils.py
# Utility functions for ebook formatting and cleaning

def clean_text(text: str) -> str:
    """
    Cleans extra spaces and ensures proper formatting.
    """
    lines = text.split("\n")
    cleaned = [line.strip() for line in lines if line.strip() != ""]
    return "\n".join(cleaned)

def shorten(text: str, max_len: int = 120) -> str:
    """
    Shortens long lines so they fit inside PDF width.
    """
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."

def build_section_dict(section_name: str, text: str, image_url: str) -> dict:
    """
    Standardize section structure for PDF compiler.
    """
    return {
        "section_name": section_name,
        "text": clean_text(text),
        "image_url": image_url
    }
