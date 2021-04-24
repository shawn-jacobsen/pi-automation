from flask import Flask, request

app = Flask(__name__)

@app.route('/api/')
def welcome():
    return "Welcome to Shawn's personal API!"

@app.route('/api/sleep-data', methods=['POST'])
def print_data():
    print(request.form)
    return "works"

if __name__ == "__main__":
    app.run(debug=True)