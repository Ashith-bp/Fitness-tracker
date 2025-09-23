from flask import Flask, request, jsonify
from models import Database
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
db = Database()

def json_date(d):
    return d.isoformat() if hasattr(d, 'isoformat') else d

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    name = data.get('name'); email = data.get('email')
    if not name or not email:
        return jsonify({'error':'name and email required'}),400
    age = data.get('age'); weight = data.get('weight_kg'); height = data.get('height_cm')
    try:
        new_id = db.insert('INSERT INTO users (name,email,age,weight_kg,height_cm) VALUES (%s,%s,%s,%s,%s)', (name,email,age,weight,height))
    except Exception as e:
        return jsonify({'error': str(e)}),400
    return jsonify({'id':new_id,'name':name,'email':email}),201

@app.route('/users/<int:uid>', methods=['GET'])
def get_user(uid):
    rows = db.query_all('SELECT id,name,email,age,weight_kg,height_cm,created_at FROM users WHERE id=%s', (uid,))
    if not rows:
        return jsonify({'error':'not found'}),404
    return jsonify(rows[0])

@app.route('/workouts', methods=['POST','GET'])
def workouts():
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        date = request.args.get('date')
        q = 'SELECT id,user_id,exercise,duration_minutes,calories_burned,workout_date FROM workouts WHERE 1=1'
        params = []
        if user_id:
            q += ' AND user_id=%s'; params.append(user_id)
        if date:
            q += ' AND workout_date=%s'; params.append(date)
        q += ' ORDER BY workout_date DESC'
        rows = db.query_all(q, tuple(params))
        return jsonify(rows)
    else:
        data = request.get_json() or {}
        user_id = data.get('user_id'); exercise = data.get('exercise'); duration = data.get('duration_minutes',0); calories = data.get('calories_burned',0); workout_date = data.get('workout_date')
        if not user_id or not exercise or not workout_date:
            return jsonify({'error':'user_id, exercise and workout_date required'}),400
        new_id = db.insert('INSERT INTO workouts (user_id,exercise,duration_minutes,calories_burned,workout_date) VALUES (%s,%s,%s,%s,%s)', (user_id,exercise,duration,calories,workout_date))
        return jsonify({'id':new_id}),201

@app.route('/meals', methods=['POST','GET'])
def meals():
    if request.method == 'GET':
        user_id = request.args.get('user_id'); date = request.args.get('date')
        q = 'SELECT id,user_id,meal_name,calories,protein_g,carbs_g,fats_g,meal_date FROM meals WHERE 1=1'
        params = []
        if user_id:
            q += ' AND user_id=%s'; params.append(user_id)
        if date:
            q += ' AND meal_date=%s'; params.append(date)
        q += ' ORDER BY meal_date DESC'
        rows = db.query_all(q, tuple(params))
        return jsonify(rows)
    else:
        data = request.get_json() or {}
        user_id = data.get('user_id'); meal_name = data.get('meal_name'); calories = data.get('calories',0); protein = data.get('protein_g',0); carbs = data.get('carbs_g',0); fats = data.get('fats_g',0); meal_date = data.get('meal_date')
        if not user_id or not meal_name or not meal_date:
            return jsonify({'error':'user_id, meal_name and meal_date required'}),400
        new_id = db.insert('INSERT INTO meals (user_id,meal_name,calories,protein_g,carbs_g,fats_g,meal_date) VALUES (%s,%s,%s,%s,%s,%s,%s)', (user_id,meal_name,calories,protein,carbs,fats,meal_date))
        return jsonify({'id':new_id}),201

@app.route('/weight', methods=['POST','GET'])
def weight_history():
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error':'user_id required'}),400
        rows = db.query_all('SELECT id,weight_kg,recorded_at FROM weight_history WHERE user_id=%s ORDER BY recorded_at DESC', (user_id,))
        return jsonify(rows)
    else:
        data = request.get_json() or {}
        user_id = data.get('user_id'); weight = data.get('weight_kg'); recorded_at = data.get('recorded_at')
        if not user_id or weight is None or not recorded_at:
            return jsonify({'error':'user_id, weight_kg and recorded_at required'}),400
        new_id = db.insert('INSERT INTO weight_history (user_id,weight_kg,recorded_at) VALUES (%s,%s,%s)', (user_id,weight,recorded_at))
        return jsonify({'id':new_id}),201

@app.route('/summary', methods=['GET'])
def summary():
    user_id = request.args.get('user_id'); date = request.args.get('date')
    if not user_id or not date:
        return jsonify({'error':'user_id and date required'}),400
    meals = db.query_all('SELECT COALESCE(SUM(calories),0) as calories_in FROM meals WHERE user_id=%s AND meal_date=%s', (user_id,date))
    workouts = db.query_all('SELECT COALESCE(SUM(calories_burned),0) as calories_out FROM workouts WHERE user_id=%s AND workout_date=%s', (user_id,date))
    return jsonify({'date':date,'calories_in': meals[0]['calories_in'],'calories_out':workouts[0]['calories_out']})

@app.route('/health', methods=['GET'])
def health():
    try:
        db.ping()
        return jsonify({'status':'ok'})
    except Exception as e:
        return jsonify({'status':'error','detail':str(e)}),500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT',5000)), debug=True)
