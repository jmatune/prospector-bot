import os
from flask import Flask, jsonify, request
from mangum import Mangum
from asgiref.wsgi import WsgiToAsgi
from discord_interactions import verify_key_decorator

DISCORD_PUBLIC_KEY = os.environ.get("DISCORD_PUBLIC_KEY")

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)
handler = Mangum(asgi_app)


@app.route("/", methods=["POST"])
async def interactions():
    print(f"Request: {request.json}")
    raw_request = request.json
    return interact(raw_request)


@verify_key_decorator(DISCORD_PUBLIC_KEY)
def interact(raw_request):
    # discord health check
    if raw_request["type"] == 1:  # PING
        response_data = {"type": 1}  # PONG
    else:
        data = raw_request["data"]
        command_name = data["name"]

        # call appropriate function
        command_func_map = {
            'hello': hello,
            'prospect_status': get_prospect_status
        }
        response_message = command_func_map[command_name]()

        response_data = {
            "type": 4,
            "data": {"content": response_message},
        }

    return jsonify(response_data)

def hello():
    return "Hello there!"

def get_prospect_status():
    return "Sorry, this feature isn't complete yet :("

if __name__ == "__main__":
    app.run(debug=True)
