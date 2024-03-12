from flask import Flask, render_template, request, redirect, url_for
import webbrowser as web
import speech_recognition as sr
import urllib.parse

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def voice_search():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print('Speak anything : ')
            audio = r.listen(source)  # records from mic
        query = r.recognize_google(audio)  # recognize voice
        print('You said :{}'.format(query))
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        return redirect(url_for('results', search_url=search_url))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return "Sorry, an error occurred during the voice search."

@app.route('/results')
def results():
    search_url = request.args.get('search_url')
    return redirect(search_url)

if __name__ == "__main__":
    app.run(debug=True)
