from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from myapp.core.functions.auth import user_logout_func, registration_func, user_login_func, get_shops
from myapp.core.functions.user import get_all_users_with_coordinates
from flask import jsonify, request, render_template

from myapp.core.routes.main import main

auth = Blueprint('auth', __name__)
methods = ['GET', 'POST']
template_folder = 'pages/auth'
redirect_url = 'main.main_view'


@auth.route('/registration', methods=methods)
def registration_view():
    template = f'{template_folder}/registration.html'

    if current_user.is_authenticated:
        return redirect(url_for(redirect_url))

    if request.method == 'GET':
        form = registration_func(request)
        return render_template(template, form=form)
    else:
        add_new_user = registration_func(request)
        if not add_new_user:
            return redirect(url_for('auth.registration_view'))
        else:
            return redirect(url_for(redirect_url))


@auth.route('/login', methods=methods)
def user_login_view():
    template = f'{template_folder}/login.html'

    if current_user.is_authenticated:
        return redirect(url_for(redirect_url))

    if request.method == 'GET':
        form = user_login_func(request)
        return render_template(template, form=form)
    else:
        user_login = user_login_func(request)
        if user_login:
            return redirect(url_for(redirect_url))
        else:
            return redirect(url_for('auth.user_login_view'))


@auth.route('/logout', methods=['GET'])
@login_required
def user_logout_view():
    user_logout_func()
    return redirect(url_for(redirect_url))


@main.route('/get_nearby_shops', methods=["POST"])
def get_nearby_shops():
    data = request.get_json()
    latitude = data['lat']
    longitude = data['lon']
    shops = get_shops(latitude, longitude)


    shops_data = [{'lat': float(node.lat), 'lon': float(node.lon), 'name': node.tags.get('name', 'Unknown Shop')} for
                  node in shops.nodes]

    return jsonify(shops_data)


@main.route('/map')
def map_view():
    users_with_coordinates = get_all_users_with_coordinates()
    return render_template('pages/map/map.html', usersWithCoordinates=users_with_coordinates)
