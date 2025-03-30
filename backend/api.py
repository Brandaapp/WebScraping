from flask import Flask, jsonify, request
import json
import scrape_hospitality
import TheJustice_Features
import Hoot_Articles

app = Flask(__name__)

@app.route('/dining_hours', methods=['GET'])
def dining_hours():
    date = request.args.get('date', "")
    output = scrape_hospitality.add_hours(date)
    return jsonify(json.loads(output))

@app.route('/justice_features', methods=['GET'])
def justice_features():
    output = TheJustice_Features.get_articles()
    return jsonify(json.loads(output))

@app.route('/hoot_articles', methods=['GET'])
def hoot_articles():
    output = Hoot_Articles.get_news_data()
    return jsonify(json.loads(output))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)