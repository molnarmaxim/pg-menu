from flask import Flask, request, jsonify, render_template
import requests
from datetime import datetime

app = Flask(__name__)

api = "https://kiosk.pg-tech.hu/monitor/data/data.json"

WEEKDAYS_HU = {
    0: 'Hétfő',
    1: 'Kedd', 
    2: 'Szerda',
    3: 'Csütörtök',
    4: 'Péntek',
    5: 'Szombat',
    6: 'Vasárnap'
}

@app.route('/')
def fooldal():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    response = requests.get(api)
    if response.status_code == 200:
        data = response.json()
        menu_data = data.get("menu", [])
        
        for item in menu_data:
            date_str = item['start']
            date_obj = datetime.strptime(date_str, '%Y.%m.%d')
            weekday = WEEKDAYS_HU[date_obj.weekday()]
            item['start'] = f"{date_str[5:]} ({weekday})"
            
        return jsonify({"menu": menu_data})
    else:
        return jsonify({"error": ""}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)