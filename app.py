from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

# PostgreSQL connection
def get_connection():
    return psycopg2.connect(
        dbname="26sqlll",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

# Query dictionary
QUERIES = {
    # --- Sample Queries ---
    "Sample 1 - Total Records": "SELECT COUNT(*) AS total_records FROM Dataset;",
    "Sample 2 - Avg Value by Category": "SELECT category, AVG(value) AS average_value FROM Dataset GROUP BY category;",
    "Sample 3 - High Value Records": "SELECT * FROM Dataset WHERE value > 8000;",
    "Sample 4 - All Analysts": "SELECT * FROM Users WHERE role = 'Analyst';",
    "Sample 5 - Logs of User 5": "SELECT * FROM analysis_logs WHERE user_id = 5;",
    "Sample 6 - Daily Average Value": "SELECT date_trunc('day', timestamp) AS day, AVG(value) AS avg_value FROM Dataset GROUP BY day ORDER BY day;",
    "Sample 7 - Categories with >30 Records": "SELECT category, COUNT(*) AS record_count FROM Dataset GROUP BY category HAVING COUNT(*) > 30;",
    "Sample 8 - Top 3 Frequent Labels": "SELECT label, COUNT(*) AS freq FROM Dataset GROUP BY label ORDER BY freq DESC LIMIT 3;",
    "Sample 9 - Top 5 by Category": """
        SELECT * FROM (
            SELECT *, RANK() OVER (PARTITION BY category ORDER BY value DESC) AS rnk FROM Dataset
        ) ranked WHERE rnk <= 5;
    """,
    "Sample 10 - Mean by Label": "SELECT label, AVG(value) AS mean_value FROM Dataset GROUP BY label ORDER BY mean_value DESC;",
    "Sample 11 - Min/Max Timestamp": "SELECT MIN(timestamp) AS earliest, MAX(timestamp) AS latest FROM Dataset;",
    "Sample 12 - Logs with User Names": """
        SELECT a.log_id, u.name, u.role, a.operation, a.log_time
        FROM analysis_logs a
        JOIN Users u ON a.user_id = u.user_id
        ORDER BY a.log_time DESC;
    """,
    "Sample 13 - Operation Count per User": """
        SELECT u.name, COUNT(*) AS operations_count
        FROM analysis_logs a
        JOIN Users u ON a.user_id = u.user_id
        GROUP BY u.name
        ORDER BY operations_count DESC;
    """,
    "Sample 14 - Label Distribution": """
        SELECT category, label, COUNT(*) AS count
        FROM Dataset
        GROUP BY category, label
        ORDER BY category, count DESC;
    """,
    "Sample 15 - Users with >5 Ops": """
        SELECT u.user_id, u.name, COUNT(*) AS operation_count
        FROM analysis_logs a
        JOIN Users u ON a.user_id = u.user_id
        GROUP BY u.user_id, u.name
        HAVING COUNT(*) > 5;
    """,
    "Sample 16 - Latest 10 Records": "SELECT * FROM Dataset ORDER BY timestamp DESC LIMIT 10;",
    "Sample 17 - Outliers via Std Dev": """
        SELECT * FROM Dataset
        WHERE value > (SELECT AVG(value) + 2 * STDDEV(value) FROM Dataset)
           OR value < (SELECT AVG(value) - 2 * STDDEV(value) FROM Dataset);
    """,
    "Sample 18 - Top Label per Category": """
        SELECT category, label, count FROM (
            SELECT category, label, COUNT(*) AS count,
                   RANK() OVER (PARTITION BY category ORDER BY COUNT(*) DESC) AS rank
            FROM Dataset GROUP BY category, label
        ) ranked WHERE rank = 1;
    """,
    "Sample 19 - Activity on Specific Day": """
        SELECT u.name, a.operation, a.log_time
        FROM analysis_logs a
        JOIN Users u ON a.user_id = u.user_id
        WHERE DATE(a.log_time) = '2025-07-25';
    """,
    "Sample 20 - Avg Value by Day & Category": """
        SELECT date_trunc('day', timestamp) AS day, category, AVG(value) AS avg_value
        FROM Dataset
        GROUP BY day, category
        ORDER BY day, category;
    """,

    # --- Nested Queries ---
    "Nested Query 1 - Top 5 by Category": """
        SELECT * FROM (
            SELECT *, RANK() OVER (PARTITION BY category ORDER BY value DESC) AS rank
            FROM Dataset
        ) ranked
        WHERE rank <= 5;
    """,
    "Nested Query 2 - Compare Mean Values": "SELECT category, AVG(value) AS mean_value FROM Dataset GROUP BY category ORDER BY mean_value DESC;",
    "Nested Query 3 - Frequent Labels": """
        SELECT category, label, count FROM (
            SELECT category, label, COUNT(*) AS count,
                   RANK() OVER (PARTITION BY category ORDER BY COUNT(*) DESC) AS rank
            FROM Dataset GROUP BY category, label
        ) ranked WHERE rank = 1;
    """,

    # --- Join Queries ---
    "Join Query 1 - Logs with User Info": """
        SELECT a.log_id, u.user_id, u.name AS user_name, u.role, a.operation, a.log_time
        FROM analysis_logs a
        JOIN Users u ON a.user_id = u.user_id
        ORDER BY a.log_time DESC;
    """,
    "Join Query 2 - Analyst Daily Activity": """
        SELECT date_trunc('day', a.log_time) AS activity_day, COUNT(*) AS total_operations
        FROM analysis_logs a
        JOIN Users u ON a.user_id = u.user_id
        WHERE u.role = 'Analyst'
        GROUP BY activity_day
        ORDER BY activity_day;
    """,
    "Join Query 3 - Category vs Label": """
        SELECT category, label, COUNT(*) AS count
        FROM Dataset
        GROUP BY category, label
        ORDER BY category, count DESC;
    """
}


@app.route('/')
def index():
    return render_template('index.html', queries=QUERIES)

@app.route('/get_query', methods=['POST'])
def get_query():
    key = request.form['query_key']
    return QUERIES[key]

@app.route('/get_output', methods=['POST'])
def get_output():
    key = request.form['query_key']
    query = QUERIES[key]

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({'columns': columns, 'rows': rows})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
