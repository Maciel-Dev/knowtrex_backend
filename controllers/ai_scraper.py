from starlette.responses import JSONResponse
from services.ai_scraper import ai_search

async def get_product_ai(url: str = "", description: str = ""):
    """Get AI-powered product search results"""
    try:
        response = await ai_search(url, description)
        # Return the raw response for now, you can process it as needed
        return {"status": "success", "data": response}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )
