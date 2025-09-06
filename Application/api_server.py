from flask import Flask, request, jsonify
from flask_cors import CORS

from load import loader, getArticle
from preprocessing import clean

title_mod, text_mod, config = loader()


app = Flask(__name__)
CORS(app)

@app.route("/check-url")
def check_url():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400
    
    url = url.strip('"')
    
    title, text = getArticle(url, config)
    if not title or not text:
        return jsonify({"error": "Unable to extract article"}), 422

    title_score = title_mod.predict_proba([title])[0][0]
    text_score = text_mod.predict_proba([text])[0][0]
    weighted_score = (0.8 * text_score) + (0.2 * title_score)
    
    is_real = weighted_score < 0.75
    title = str(title)
    is_real = str(is_real)

    return jsonify({
        "title": title,
        "title_score": title_score,
        "text_score": text_score,
        "weighted_score": weighted_score,
        "is_real": is_real
    })

def run_api():
    app.run(port=5000, debug=False)