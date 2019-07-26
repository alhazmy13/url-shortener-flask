import random
import string
import logging

from app.extenstions import redis
from flask import (Blueprint, request, current_app,
                   render_template, flash, redirect,
                   url_for)

api = Blueprint('short_url', __name__)
log = logging.getLogger(__name__)


def gen_short_key(length=8):
    valid_chars = string.ascii_letters + string.digits
    short_key = ''
    for i in range(length):
        short_key += random.SystemRandom().choice(valid_chars)
    return short_key


def get_full_url(key):
    try:
        return redis.get(key).decode('utf-8')
    except Exception as ex:
        log.debug(ex)
        return None


def insert_data(short_url, full_url):
    try:
        redis.set(short_url, full_url)
        return True
    except Exception as ex:
        log.debug(ex)
        return False


@api.route('/')
def index():
    return render_template('index.html')


@api.route('/', methods=['POST'])
def insert_route():
    site_url = current_app.config['SITE_URL']
    furl = request.form['full_url']
    if current_app.config['KEY_LENGTH']:
        s_key = gen_short_key(current_app.config['KEY_LENGTH'])
    else:
        s_key = gen_short_key()

    if site_url.endswith('/'):
        s_url = site_url + s_key
    else:
        s_url = site_url + '/' + s_key

    if insert_data(s_key, furl):
        return render_template('index.html', full_url=furl, short_url=s_url)
    else:
        flash('Error encountered saving data')
        return redirect(url_for('short_url.index'))


@api.route('/<url_key>/', methods=['GET'])
def expand_url(url_key):
    full_url = get_full_url(url_key)
    if full_url:
        return redirect(full_url)
    else:
        flash('Redirect failed: Invalid or missing short URL')
        return redirect(url_for('short_url.index'))
