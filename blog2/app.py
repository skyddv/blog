from m import Application
from blog2.models import db

app = Application()
app.register_extension(db)

if __name__ == '__main__':
    db.metadata.create_all()
