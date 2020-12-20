from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route('/')
def render_home():
    """
    Renders the dev_gui_home.html template
    Returns:
        htmlcode(str): HTML code for the page
    """
    return render_template('dev_gui_home.html')
