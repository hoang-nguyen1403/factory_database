from flask import Flask

# init app
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello,world'

