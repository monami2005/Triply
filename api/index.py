import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from .models import db, Trip, Member, Expense, ExpenseParticipant, MessageTemplate, Setting
from .database import init_db
from .logic import calculate_trip_balances, format_whatsapp_message
from datetime import datetime

app = Flask(__name__)

# SQLITE for local, can be replaced by postgres for production
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tripsplit.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "version": "v2.2"})

# --- TRIP ROUTES ---

@app.route('/api/trips', methods=['GET', 'POST'])
def handle_trips():
    if request.method == 'POST':
        data = request.json
        new_trip = Trip(
            name=data.get('name'),
            location=data.get('location'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date')
        )
        db.session.add(new_trip)
        db.session.commit()
        return jsonify({"id": new_trip.id, "message": "Trip created successfully"})
    
    trips = Trip.query.order_by(Trip.created_at.desc()).all()
    return jsonify([{
        "id": t.id, 
        "name": t.name, 
        "location": t.location,
        "start_date": t.start_date,
        "end_date": t.end_date
    } for t in trips])

@app.route('/api/trips/<trip_id>', methods=['GET', 'DELETE'])
def handle_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if request.method == 'DELETE':
        db.session.delete(trip)
        db.session.commit()
        return jsonify({"message": "Trip deleted"})
    
    stats = calculate_trip_balances(trip)
    return jsonify({
        "id": trip.id,
        "name": trip.name,
        "location": trip.location,
        "stats": stats
    })

# --- MEMBER ROUTES ---

@app.route('/api/trips/<trip_id>/members', methods=['GET', 'POST'])
def handle_members(trip_id):
    if request.method == 'POST':
        data = request.json
        new_member = Member(
            trip_id=trip_id,
            name=data.get('name'),
            whatsapp_number=data.get('whatsapp_number'),
            photo_url=data.get('photo_url') # In a real app, this would be a file upload path
        )
        db.session.add(new_member)
        db.session.commit()
        return jsonify({"id": new_member.id, "message": "Member added"})
    
    members = Member.query.filter_by(trip_id=trip_id).all()
    return jsonify([{
        "id": m.id, 
        "name": m.name, 
        "whatsapp_number": m.whatsapp_number,
        "photo_url": m.photo_url
    } for m in members])

@app.route('/api/members/<member_id>', methods=['PUT', 'DELETE'])
def handle_member(member_id):
    member = Member.query.get_or_404(member_id)
    if request.method == 'DELETE':
        db.session.delete(member)
        db.session.commit()
        return jsonify({"message": "Member deleted"})
    
    data = request.json
    member.name = data.get('name', member.name)
    member.whatsapp_number = data.get('whatsapp_number', member.whatsapp_number)
    member.photo_url = data.get('photo_url', member.photo_url)
    db.session.commit()
    return jsonify({"message": "Member updated"})

# --- EXPENSE ROUTES ---

@app.route('/api/trips/<trip_id>/expenses', methods=['GET', 'POST'])
def handle_expenses(trip_id):
    if request.method == 'POST':
        data = request.json
        new_expense = Expense(
            trip_id=trip_id,
            title=data.get('title'),
            amount=float(data.get('amount')),
            date=data.get('date'),
            payer_id=data.get('payer_id')
        )
        db.session.add(new_expense)
        db.session.flush() # Get ID before commit
        
        participant_ids = data.get('apply_to', [])
        for p_id in participant_ids:
            participant = ExpenseParticipant(expense_id=new_expense.id, member_id=p_id)
            db.session.add(participant)
        
        db.session.commit()
        return jsonify({"id": new_expense.id, "message": "Expense added"})

    expenses = Expense.query.filter_by(trip_id=trip_id).order_by(Expense.date.desc()).all()
    return jsonify([{
        "id": e.id,
        "title": e.title,
        "amount": e.amount,
        "date": e.date,
        "payer_name": Member.query.get(e.payer_id).name,
        "participants": [p.member.name for p in e.participants]
    } for e in expenses])

# --- TEMPLATE & SETTINGS ---

@app.route('/api/templates', methods=['GET', 'POST'])
def handle_templates():
    if request.method == 'POST':
        data = request.json
        new_tmpl = MessageTemplate(
            name=data.get('name'),
            content=data.get('content'),
            is_default=data.get('is_default', False)
        )
        if new_tmpl.is_default:
            MessageTemplate.query.update({MessageTemplate.is_default: False})
        db.session.add(new_tmpl)
        db.session.commit()
        return jsonify({"message": "Template saved"})
    
    templates = MessageTemplate.query.all()
    return jsonify([{"id": t.id, "name": t.name, "content": t.content, "is_default": t.is_default} for t in templates])

@app.route('/api/settings', methods=['GET', 'PUT'])
def handle_settings():
    setting = Setting.query.first()
    if request.method == 'PUT':
        data = request.json
        setting.timezone = data.get('timezone', setting.timezone)
        setting.currency = data.get('currency', setting.currency)
        setting.theme = data.get('theme', setting.theme)
        db.session.commit()
        return jsonify({"message": "Settings updated"})
    
    return jsonify({
        "timezone": setting.timezone,
        "currency": setting.currency,
        "theme": setting.theme
    })

if __name__ == '__main__':
    app.run(debug=True)
