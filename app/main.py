from fastapi import FastAPI
from routers.article import router as router_article
#from routers.comment import router as router_comment
from routers.user import router as router_user
from auth import router as router_auth


app=FastAPI()


#app.include_router(router=router_comment)
app.include_router(router=router_user)
app.include_router(router=router_auth)
app.include_router(router=router_article)


