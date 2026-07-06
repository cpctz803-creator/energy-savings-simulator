import math

# 建物タイプ別の定数データ
BUILDING_DATA = {
    "1": {"name": "事務所",   "led_w": 6.0, "led_h": 3000, "hvac_kwh": 35, "vent_vol": 5.0,  "vent_h": 3000},
    "2": {"name": "病院",     "led_w": 5.0, "led_h": 5000, "hvac_kwh": 75, "vent_vol": 6.0,  "vent_h": 5000},
    "3": {"name": "学校",     "led_w": 5.5, "led_h": 2000, "hvac_kwh": 25, "vent_vol": 10.0, "vent_h": 2000},
    "4": {"name": "ホテル",   "led_w": 4.5, "led_h": 6000, "hvac_kwh": 80, "vent_vol": 4.0,  "vent_h": 6000},
    "5": {"name": "商業施設", "led_w": 9.0, "led_h": 4000, "hvac_kwh": 90, "vent_vol": 8.0,  "vent_h": 4000}
}

def calculate_savings(type_num, area, has_led, has_eco_hvac, has_total_heat_ex, rate=28):
    """省エネ削減計算ロジック"""
    data = BUILDING_DATA.get(type_num)
    if not data: return None
    
    CO2_FACTOR = 0.441 # kg-CO2/kWh

    # 1. 照明の計算 (LED化による削減)
    new_lighting_kwh = (area * data["led_w"] * data["led_h"]) / 1000
    cur_lighting_kwh = new_lighting_kwh if has_led else new_lighting_kwh * 2.5
    
    # 2. 換気の計算
    vent_units = math.ceil((area * data["vent_vol"]) / 500)
    new_vent_kwh = (vent_units * 150 * data["vent_h"]) / 1000
    if has_total_heat_ex:
        cur_vent_kwh = new_vent_kwh
        hvac_penalty = 1.0
    else:
        cur_vent_kwh = (vent_units * 100 * data["vent_h"]) / 1000
        hvac_penalty = 1.3 # 普通換気による外気負荷増
        
    # 3. 空調の計算
    new_hvac_kwh = area * data["hvac_kwh"]
    cur_hvac_kwh = (new_hvac_kwh if has_eco_hvac else new_hvac_kwh * 1.5) * hvac_penalty

    # 集計
    cur_total = cur_lighting_kwh + cur_hvac_kwh + cur_vent_kwh
    new_total = new_lighting_kwh + new_hvac_kwh + new_vent_kwh
    diff_kwh = cur_total - new_total
    
    return {
        "name": data["name"],
        "cur_total": round(cur_total),
        "new_total": round(new_total),
        "diff_kwh": round(diff_kwh),
        "diff_cost": round(diff_kwh * rate),
        "diff_co2": round(diff_kwh * CO2_FACTOR / 1000, 2),
        "details": {
            "lighting": round(cur_lighting_kwh - new_lighting_kwh),
            "hvac": round(cur_hvac_kwh - new_hvac_kwh),
            "vent": round(cur_vent_kwh - new_vent_kwh)
        }
    }