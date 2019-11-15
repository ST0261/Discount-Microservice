from Discount_handler.discount_handler import discount_router

from flask import Flask


app = Flask(__name__)           #Creating an App instance

app.register_blueprint(discount_router)


@app.route("/")
def hello():
    return "Discounts server"

if __name__ == "__main__":      #On running python app.py
    app.run('0.0.0.0',debug=True)         #Run the flask App