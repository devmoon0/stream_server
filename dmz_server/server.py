## ref : http://wandlab.com/blog/?p=94
from flask import Flask, request, Response, stream_with_context
import os, requests, json
from streamer import Streamer

import os
from loguru import logger
base_dir = os.path.join(os.getcwd(), 'logs')
config_dict = dict(
    rotation="00:00",
    format="[{time:YYYY-MM-DD HH:mm:ss}] | {level} | {message}",
    retention="7 days",
    compression="tar",
    encoding="utf8"
)

logger.add(os.path.join(base_dir, 'myGUI_{time:YYYY-MM-DD}.log'), level="INFO", **config_dict)


app = Flask( __name__ )
streamer = Streamer(logger)


@app.route('/test')
def test():
    logger.info("test")
    return {'res': 'hi'}

@app.route('/stream')
def stream():
    src = request.args.get('src', type = str)
    try :
        return Response(
            stream_with_context(stream_gen(src)),
            mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e :
        logger.exception(f'stream error : {str(e)}')

# 내부로 사진 전송
def sendToServer(file, datas, aliases):
    try:
        datas['aliases'] = aliases
        # logger.info(f'[sendToServer] {aliases} Send')
        files = [
                ('document', (datas['filename'], file, 'application/octet-stream')),
                ('datas', ('datas', json.dumps(datas), 'application/json')),
            ]
        send_url = f'http://127.0.0.1:5000/send/{aliases}'
        try:
            requests.post(send_url, timeout= 20, files = files, stream=True)
        except Exception as e:
            return
    except Exception as e:
        logger.exception(f'[sendToServer] {e}')

@app.route('/stream/CCTV8')
def streamCCTV8():
    end_url = 'cctv8'
    src = "myURL"
    try :
        return Response(
            stream_with_context(stream_gen(src, end_url)),
            mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e :
        logger.exception(f'stream error : {str(e)}')


def stream_gen(src, end_url=None):
    try :
        streamer.run(src)
        while True :
            frame = streamer.bytescode()
            if end_url:
                try:
                    sendToServer(frame, {"filename":src}, end_url)
                except print(0):
                    pass
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except GeneratorExit :
        logger.exception('disconnected stream')
        streamer.stop()

if __name__ == '__main__' :
    logger.info('------------------------------------------------')
    logger.info('START')
    logger.info('------------------------------------------------')
    app.run( host='0.0.0.0', port=5000, debug=False, threaded=True)
