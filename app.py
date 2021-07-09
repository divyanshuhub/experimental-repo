from flask import Flask
import final_run

app = Flask(__name__)

@app.route('/')
def dynamic_page():
    return final_run.funs()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)
