from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

base_router = APIRouter()


@base_router.get('/robots.txt', response_class=PlainTextResponse, tags=['BASE'])
def robots():
    return """User-agent: *\nDisallow: /"""
