from app import app 

from app.controllers.users import users
from app.controllers.lists import lists

app.register_blueprint(users)
app.register_blueprint(lists)


if __name__ == "__main__":
    app.run(debug=True)