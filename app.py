from define_app import create_app
from model.models import db

my_app = create_app()
db.init_app(my_app)

if __name__ == "__main__":
    my_app.run()