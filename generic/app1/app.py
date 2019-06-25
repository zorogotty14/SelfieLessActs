from flask import Flask, url_for,jsonify,abort
from flask import request
from flask import abort
app = Flask(__name__)

@app.route("/")
def hello():
    return 200


@app.route("/app1/new", methods=["GET","POST","DELETE"])
def newmethod():
	return jsonify({"Request":request.method}), 200


if __name__=="__main__":
	app.run(host="0.0.0.0", port=80)




