from flask import Flask, render_template, request
from logic import calculate_savings, BUILDING_DATA

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            type_num = request.form.get('building_type')
            area = float(request.form.get('area', 0))
            has_led = 'has_led' in request.form
            has_eco_hvac = 'has_eco_hvac' in request.form
            has_total_heat_ex = 'has_total_heat_ex' in request.form
            
            result = calculate_savings(type_num, area, has_led, has_eco_hvac, has_total_heat_ex)
        except ValueError:
            pass # エラー処理は必要に応じて

    return render_template('index.html', result=result, buildings=BUILDING_DATA)

if __name__ == '__main__':
    app.run(debug=True)