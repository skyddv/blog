from m import Application
from m.security import AuthenticationFilter

from blog2.authentication import JWTAuthenticationProvider
from blog2.handlers.user import router as user
from blog2.handlers.post import router as post
from blog2.handlers.comment import router as comment
from blog2.handlers.catalog import router as catalog
from blog2.models import db

app = Application()
app.register_extension(db)
app.add_filter(AuthenticationFilter(JWTAuthenticationProvider))
app.add_router(user)
app.add_router(post)
app.add_router(catalog)
app.add_router(comment)

if __name__ == '__main__':
    # db.metadata.drop_all()
    # db.metadata.create_all()
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8080, app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()