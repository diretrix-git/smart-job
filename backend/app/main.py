from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.resumes import router as resumes_router
from app.api.recommendations import router as recommendations_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(resumes_router, prefix=f"{settings.API_V1_STR}/resumes", tags=["resumes"])
app.include_router(recommendations_router, prefix=f"{settings.API_V1_STR}/recommendations", tags=["recommendations"])

@app.get("/")
def root():
    return {"message": "Welcome to the Smart Job Recommendation API"}
