from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.config import client, env, fastapi_config
from app.charts.router import router as charts_router
from app.birthday_information.router import router as birthday_information_router
from app.question.router import router as question_router
from app.chat.router import router as chat_router
app = FastAPI(**fastapi_config)


@app.on_event("shutdown")
def shutdown_db_client():
    client.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=env.CORS_ORIGINS,
    allow_methods=env.CORS_METHODS,
    allow_headers=env.CORS_HEADERS,
    allow_credentials=True,
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(charts_router, prefix="/charts", tags=["Natal Charts"])
app.include_router(birthday_information_router, prefix="/birthday_information", tags=["Birthday Information"])
app.include_router(question_router, prefix="/question", tags=["Generate Astrology Question"])
app.include_router(chat_router, prefix="/chat", tags=["ChatGPT Chat"])




