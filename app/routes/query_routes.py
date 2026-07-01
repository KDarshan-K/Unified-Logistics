from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/admin")
def admin_page(request: Request):
    from app.main import templates
    return templates.TemplateResponse("admin.html", {"request": request})

@router.post("/admin/query")
def admin_query(data: dict):
    from app.services.query_service import run_natural_language_query
    question = data.get("question", "").strip()
    if not question:
        return JSONResponse({"error": "No question provided"}, status_code=400)
    return run_natural_language_query(question)