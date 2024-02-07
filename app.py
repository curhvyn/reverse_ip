from flask import Flask, request, jsonify
import os
import psycopg2


app = Flask(__name__)

# Get database path from environment variable or use default value
DB_PATH = os.getenv('DB_PATH', 'reverse_ips.db')

# Function to establish database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        return conn
    except Exception as e:
        app.logger.error(f"Database connection error: {str(e)}")
        return None

@app.route('/')
def get_reverse_ip():
    try:
        origin_ip = request.remote_addr
        reversed_ip = '.'.join(reversed(origin_ip.split('.')))

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO reverse_ips (ip_address) VALUES (%s)", (reversed_ip,))
            conn.commit()
            conn.close()

        return jsonify({"reverse_ip": reversed_ip}), 200
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
