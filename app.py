from flask import Flask
from sqlalchemy import true

# creating an instance of class Flask
app = Flask(__name__)


# the first base page
@app.route('/')
def base():
    return "ahoj"



if __name__ == '__main__':
    app.run()