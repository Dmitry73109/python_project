import time
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# СЃРїРёСЃРѕРє РєРѕРјРЅР°С‚ РІ С„РѕСЂРјР°С‚Рµ {id РєРѕРјРЅР°С‚С‹: [СЃРїРёСЃРѕРє РїРѕР»СЊР·РѕРІР°С‚РµР»РµР№]}
rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_room', methods=['POST'])
def create_room():
    users = request.form.getlist('users')
    time_limit = int(request.form['time_limit'])
    room_id = str(len(rooms) + 1)

    rooms[room_id] = users

    time.sleep(3) # Р·Р°РґРµСЂР¶РєР° РґР»СЏ СЃС‚Р°Р±РёР»СЊРЅРѕРіРѕ РёРЅС‚РµСЂРЅРµС‚Р°

    return redirect('/room/{}'.format(room_id))

@app.route('/room/<room_id>', methods=['GET', 'POST'])
def room(room_id):
    if room_id not in rooms:
        return redirect('/')

    if request.method == 'POST':
        # РєРЅРѕРїРєР° РѕС‚РєР»СЋС‡РµРЅРёСЏ РјРёРєСЂРѕС„РѕРЅР°
        muted = request.form.get('muted')
    else:
        muted = False

    # РїСЂРѕРІРµСЂРєР° РЅР°Р»РёС‡РёСЏ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ РІ РєРѕРјРЅР°С‚Рµ
    user_id = request.args.get('user_id')
    if not user_id or user_id not in rooms[room_id]:
        return redirect('/')

    # С‚Р°Р№РјРµСЂ РЅР° Р·Р°РєСЂС‹С‚РёРµ РєРѕРјРЅР°С‚С‹
    start_time = rooms.get(room_id + '_start_time')
    if not start_time:
        rooms[room_id + '_start_time'] = time.time()
        start_time = time.time()

    remaining_time = start_time + time_limit - time.time()
    if remaining_time <= 0 or len(rooms[room_id]) == 0:
        del rooms[room_id]
        return redirect('/')

    return render_template('room.html', room_id=room_id, user_id=user_id, muted=muted, remaining_time=remaining_time)

if __name__ == '__main__':
    app.run(debug=True)