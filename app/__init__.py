from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_swagger_ui_oauth2_redirect_html,
    get_swagger_ui_html
)
from fastapi.openapi.utils import get_openapi

from app.config import settings





def create_app() -> FastAPI:
    
    app = FastAPI(
        title="Witit Post Api",
        redoc_url=None
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

    app.mount("/static", StaticFiles(directory="static"), name="static")

    # add custom openapi documentation
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title='Witit Post Api',
            version='0.1.0',
            routes=app.routes,
            servers=[
                {
                    "url": f"{settings.POST_API_HOST}"
                }
            ]
        )

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi



    # routes section here
    from app.chats import router as posts_router
    
    
    app.include_router(posts_router, tags=["Post Endpoints"])

    @app.get("/swagger-ui.html", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=f"{settings.POST_API_HOST}/openapi.json",
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=f"{settings.POST_API_HOST}/static/swagger-ui-bundle.js",
            swagger_css_url=f"{settings.POST_API_HOST}/static/swagger-ui.css",
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()


    return app