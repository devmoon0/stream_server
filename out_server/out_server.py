
## ref : http://wandlab.com/blog/?p=94
from flask import Flask, request, Response, stream_with_context

import queue

import os, json
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
class WriteableQueue(queue.Queue):
    def write(self, data):
        if not self.empty():
            try:
                self.get_nowait()
            except queue.Empty:
                pass
        if data:
            self.put(data)

    def __iter__(self):
        return iter(self.get, None)

    def close(self):
        self.put(None)

q = WriteableQueue(100)
q2 = WriteableQueue(100)
q3 = WriteableQueue(100)


@app.route('/test')
def test():
    logger.info("test")
    return {'res': 'hi'}

def stream_gen(iterable):
    try :
        while True :
            frame = iterable.get()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except GeneratorExit :
        logger.exception('disconnected stream')


@app.route('/CCTV8')
def showCCTV8():
    logger.info("*******showCCTV8***********")
    return Response(
            stream_with_context(stream_gen(q)),
            mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/send/cctv8', methods=['POST'])
def StreamCCTV8():
    try:
        posted_file = request.files['document'].read()
        posted_data_b = request.files['datas'].read()
        posted_data= json.loads(posted_data_b.decode())
        # logger.info('***** {} Image Send : {} *****'.format(posted_data['aliases'],"test"))
        q.write(posted_file)
        return {'res': 'hi'}
    except Exception as e:
        logger.error(f"[StreamCCTV8] {e}")
        q.empty()

if __name__ == '__main__' :
    logger.info('------------------------------------------------')
    logger.info('START')
    logger.info('------------------------------------------------')
    app.run( host='0.0.0.0', port=5000, debug=False, threaded=True)