from fastapi import FastAPI
from routers.article import router as router_article
from routers.comment import router as router_comment
from routers.user import router as router_user
from auth import router as router_auth
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router=router_user)
app.include_router(router=router_auth)
app.include_router(router=router_article)
app.include_router(router=router_comment)


