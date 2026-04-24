from flask import Flask, jsonify
import teradatasql

app = Flask(__name__)

@app.route('/')
def home():
    return "Unilever Data Pipeline Running"

@app.route('/data')
def get_data():
    con = teradatasql.connect(
        host="YOUR_TERADATA_HOST",
        user="YOUR_USER",
        password="YOUR_PASSWORD"
    )
    cursor = con.cursor()
    cursor.execute("SELECT * FROM sales_table")
    rows = cursor.fetchall()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
