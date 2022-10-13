from flask import Flask, request, render_template
from surprise import dump 

app = Flask(__name__)
model = dump.load('model.pkl')  # load the model

@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"

@app.route("/predict", methods=["GET"])
def predict():
    print(model)
    prediction = model[1].predict(4470)
    print(prediction)
    return "<p>Predict!</p>"

if __name__ == "__main__":
    app.run()
