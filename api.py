# import the necessary packages
import flask
import json
import mariadb

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# configuration used to connect to MariaDB
config = {
    'host': 'mariadb',
    'port': 3306,
    'user': 'root',
    'password': 'password123',
    'database': 'demo'
}

# connection for MariaDB
conn = mariadb.connect(**config)
# create a connection cursor
cur = conn.cursor()
cur.execute("select * from people")
data = cur.fetchall()

if not data:
    cur.execute("CREATE TABLE demo.people (name VARCHAR(50));")
    cur.execute(
        "INSERT INTO demo.people VALUES ('rob'), ('tracy'), ('sam'), ('duke');")

# route to return all people

@app.route("/")
def home():
    return "Hello World!"


@app.route('/api/people')
def index():
    # execute a SQL statement
    cur.execute("select * from people")

    # serialize results into JSON
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    # return the results!
    return json.dumps(json_data)


app.run(debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True)
