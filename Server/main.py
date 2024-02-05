from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/get-sound/<image_url>")
def get_sound(image_url):
    return image_url


if __name__ == "__main__":
    app.run(debug=True)