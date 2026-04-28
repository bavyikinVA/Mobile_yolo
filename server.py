import database
import socket
import json
import predict
import os
import time
import base64


def handle_request(request):
    print(f"Request: {request}")
    if request['action'] == 'register':
        request.pop('action')
        registered, current_user_id = database.add_new_user_to_db(**request)
        if registered:
            return {'status': 'success', 'current_user_id': current_user_id}
        else:
            return {'status': 'error', 'message': 'User already exists'}
    elif request['action'] == 'login':
        request.pop('action')
        check_auth = database.authenticate_user(**request)
        if check_auth == "success":
            return {'status': 'success'}
        else:
            return {'status': 'error'}
    elif request['action'] == 'insert_data':
        request.pop('action')
        flag = database.insert_data(**request)
        if flag is True:
            return {'status': 'success'}
    elif request['action'] == 'process_image':
        user_id = request['user_id']
        image_data = request['image_data']
        images_dir = f"{user_id}_images"
        os.makedirs(images_dir, exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        photo_name = f"photo_{timestamp}.jpg"
        photo_path = os.path.join(images_dir, photo_name)

        with open(photo_path, 'wb') as file:
            file.write(base64.b64decode(image_data))
        digit_array = predict.digit_detection(photo_path)
        return {'status': 'success', 'digit_array': digit_array}


def recv_all(sock, length):
    # Helper function to receive all data from a socket
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('Was expecting {!r} bytes, only received {!r} bytes '
                           'before the socket closed'.format(length, len(data)))
        data += more
    return data


def handle_connection(conn):
    # Receive the header (which contains the length of the JSON data)
    header_length = 10
    header_data = recv_all(conn, header_length)
    try:
        header = header_data.decode('utf-8')
    except UnicodeDecodeError as e:
        print(f"Error decoding header: {e}")
        conn.close()
        return

    header_int = int(header.strip())

    # Receive the JSON data
    json_data = recv_all(conn, header_int)
    try:
        decoded_json_data = json_data.decode('utf-8')
        request = json.loads(decoded_json_data)
    except UnicodeDecodeError as e:
        print(f"Error decoding JSON data: {e}")
        conn.close()
        return
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")
        conn.close()
        return

    # Handle the request and send a response
    response = handle_request(request)
    encoded_response = json.dumps(response).encode('utf-8')  # Encode the response using UTF-8
    conn.sendall(encoded_response)
    conn.close()


def start_server(host="192.168.0.10", port=8080):
    database.create_db()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server started at {host}:{port}")
        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    handle_connection(conn)
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    start_server()
