from __future__ import division

from flask import Flask, request, jsonify
from datetime import datetime


app = Flask(__name__)

entries = {}
charges = {
    'standard_rate': 10.0, 
    'increment': 15  
}

id = 0

def calculate_charge(entry_time):
    delta = datetime.now() - entry_time
    total_minutes = delta.total_seconds() / 60
    increments = (total_minutes + charges['increment'] - 1) // charges['increment']
    total_hours = increments * (charges['increment'] / 60)
    return round(total_hours * charges['standard_rate'], 2)

@app.route('/entry', methods=['POST'])
def entry():
    global id
    plate = request.args.get('plate')
    parking_lot = request.args.get('parkingLot')
    ticket_id = str(id)
    id += 1
    entries[ticket_id] = {'plate': plate, 'parkingLot': parking_lot, 'entryTime': datetime.now()}
    return jsonify({'ticketId': ticket_id}), 201

@app.route('/exit', methods=['POST'])
def exit():
    ticket_id = request.args.get('ticketId')
    entry_record = entries.pop(ticket_id, None)
    if not entry_record:
        return jsonify({'error': 'Ticket not found'}), 404
    charge = calculate_charge(entry_record['entryTime'])
    total_time_parked = datetime.now() - entry_record['entryTime']
    return jsonify({
        'licensePlate': entry_record['plate'],
        'totalParkedTime': str(total_time_parked),
        'parkingLotId': entry_record['parkingLot'],
        'charge': '${:.2f}'.format(charge)  # Using str.format for compatibility
    }), 200



@app.route("/")
def hello():
    return "<h3>Hello {name}!</h3>" \
           "<b>22:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)