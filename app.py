from flask import Flask, render_template, Response
from camera import Video
from camera_colour_mask import VideoMask

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame=camera.get_frame()
        yield(b'--frame \r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame +
              b'\r\n\r\n')

@app.route('/video')
def video():
    return Response(gen(VideoMask()),mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(debug=True,ssl_context='adhoc')