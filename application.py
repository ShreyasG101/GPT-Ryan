#flask --app application run --host=0.0.0.0

from pydub import AudioSegment
#import whisper
from flask import Flask, request, render_template, send_file
import sys
from tts import output_speech
from assistant import run

#model = whisper.load_model("base")

def create_app():

    # print a nice greeting.
    def say_hello(username = "World"):
        return '<p>Hello %s!</p>\n' % username

    # some bits of text for the page.
    header_text = '''
        <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
    instructions = '''
        <p><em>Hint</em>: This is a RESTful web service! Append a username
        to the URL (for example: <code>/Thelonious</code>) to say hello to
        someone specific.</p>\n'''
    home_link = '<p><a href="/">Back</a></p>\n'
    footer_text = '</body>\n</html>'

    # EB looks for an 'application' callable by default.
    app = Flask(__name__)

    # add a rule for the index page.
    app.add_url_rule('/', 'index', (lambda: header_text +
        say_hello() + instructions + footer_text))
    @app.route('/submit', methods=['POST', 'GET'])
    def submit():
        print("IN SUBMIT", file=sys.stderr)
        if request.method == 'POST':
            #input_save_path = upload_audio()
            #print("audio uploaded")
            #prompt = transcribe_audio(input_save_path)
            prompt = parse_dictation()

            output = run(prompt)        
            output_save_path = './audio/output_speech.mpeg'
            output_speech(output,output_save_path)
            #mpeg_to_m4a(output_save_path)
            return send_file(output_save_path)
            
        # the code below is executed if the request method
        # was GET or the credentials were invalid
        #return render_template('login.html', error=error)
        
    def upload_audio():
        print('trying to upload audio')
        iter = request.files.items()
        for file in iter:
            print(file)
        f = request.files['input']
        input_save_path = './audio/input_speech.m4a'
        f.save(input_save_path)
        return input_save_path

    def parse_dictation():
        print("parse dict")
        iter = request.files.items()
        for a in iter:
            print(a)
        f = request.files['input']
        f.seek(0)
        prompt = str(f.read(), 'utf-8')
        print(prompt)
        return prompt
    return app

    def mpeg_to_m4a(f_path):
        audio = AudioSegment.from_file(f_path, "mpeg")
        audio.export(f_path, format="m4a")


application = create_app()
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
    

"""
def transcribe_audio(f_path):
    #Convert from m4a to mp3
    audio = AudioSegment.from_file(f_path, "m4a")
    audio.export(f_path, format="mp3")
    result = model.transcribe(f_path)
    print("result")
    return result['text']


"""


