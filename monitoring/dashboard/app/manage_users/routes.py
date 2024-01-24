from datetime import datetime, timezone
from typing import Dict, List, Tuple, Set
from flask import render_template, flash, redirect, url_for, request, jsonify, abort, json
from flask.json import loads as jsonParse
from flask_login import current_user, login_required
from app.extensions import db
from app.manage_users import bp
from app.models import User
from app.manage_users.forms import ValidateUserForm, DeleteUserForm


@bp.route('/manageusers', methods=['GET'])
@login_required
def manageusers():
    
    users = User.query.all()
    permissionlevels = [{"levelname": "User", "levelnum":0},
                        {"levelname": "Organisation", "levelnum":1},
                        {"levelname": "Administrator", "levelnum":2}]


    
    
    return render_template('manage_users/manageusers.html', title='Manage Users', users = users, permlevels = permissionlevels)  

@bp.route('/<userid>/active/<active>', methods=['POST'])
def setActive(userid, active):
    if request.method == 'POST':
        try:
            user =  User.query.get(userid)
            if active == "True":
                boolean = True
            else:
                boolean = False
            user.active = boolean
            db.session.commit()
            return jsonify({'result' : 200, 'message': f'User {user.username}: active is set to {active}.' })
        except:
            db.session.rollback()
            return jsonify({'result' : 400, 'message': f'User {user.username}: Active could not be set.' })      
            


@bp.route('/<string:userid>/permlevel/<int:level>', methods=['POST'])
def setpermlevel(userid, level):
    
    if request.method == 'POST':
        try:
            user =  User.query.get(userid)
            user.permissionlevel = level
            db.session.commit()
            return jsonify({'result' : 200, 'message': f'User {user.username}: level changed to {level}.' })
        except:
            db.session.rollback()
            return jsonify({'result' : 400, 'message': f'User {user.username}: level could not change.' })        
    

@bp.route('/<string:userid>', methods=['DELETE'])
@login_required
def deleteuser(userid):

    if request.method == 'DELETE':
        try:
            db.session.query(User).filter(User.id==userid).delete()
            db.session.commit()
            return jsonify({'result' : 200, 'message': 'User successfully deleted.' })
        except:
            db.session.rollback()
            return jsonify({'result' : 400, 'message': 'User could not be deleted.' })

