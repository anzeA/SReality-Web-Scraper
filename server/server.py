import os
import time

import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)


def get_db_connection():
    dbname = os.environ.get('DB_NAME')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')

    while True:
        try:
            conn = psycopg2.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )
            return conn
        except:
            app.logger.error('Unable to reach database. Retrying in 5s...')
            time.sleep(5)
            continue


# health check endpoint
@app.route('/health', methods=['GET'])
def health():
    # log
    app.logger.debug('Health check')
    return jsonify({'message': 'OK'}), 200


def get_apartments():
    conn = get_db_connection()
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()
    # get all apartments with their images
    cur.execute("""
        SELECT a.id, a.name, i.image FROM apartments a
        LEFT JOIN apartments_images i ON a.id = i.apartment_id
    """)

    apartments = cur.fetchall()
    cur.close()
    conn.close()
    return apartments


@app.route('/', methods=['GET'])
def get_people():
    try:
        apartments = get_apartments()
        apartments = [{'id': a[0], 'name': a[1], 'image': a[2]} for a in apartments]
        appartments_join = {}
        id2name = {}
        for a in apartments:
            appartments_join.setdefault(a['id'], []).append(a['image'])
            id2name[a['id']] = a['name']
        html = ''

        html += f'<h1>Number of apartments: {len(appartments_join)}</h1>'
        for i, (id, images) in enumerate(appartments_join.items()):
            html += f'<div><p>{id2name[id]}</p>'
            for img in images:
                html += f'<img src="{img}">'
            html += '</div>'

        return html
    except Exception as e:
        app.logger.error(e)
        return '<p>No apartments found. Try refreshing the page.</p>'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
