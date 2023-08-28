from flask import Flask, render_template, session, request, redirect, url_for
from pygments import highlight
from pygments.lexers import Python3Lexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles
from playwright.sync_api import sync_playwright
from utils import take_screenshot_from_url
import base64

app = Flask(__name__)
app.secret_key = '6413f540832ffba9dfc77d22ca2ad618a64d30863f2c8b99a229e3bc49bfb5c3'
PLACEHOLDER = "print('Hello World')"
DEFAULT_STYLE = 'monokai'
NO_CODE_MESSAGE = "#No Code Entered "

@app.route('/', methods=['GET'])
def code():
    if not session.get('code'):
        session['code'] = PLACEHOLDER
    lines = session['code'].split('\n')
    context = {
        "message": "Paste your python code here ",
        "code": session['code'],
        "num_lines": len(lines),
        "max_chars": len(max(lines, key=len)),
    }
    return render_template('code_input.html', **context)

@app.route('/style', methods=['GET'])
def style():
    if not session.get('style'):
        session['style'] = DEFAULT_STYLE
    formatter = HtmlFormatter(style=session['style'])
    context = {
        "message": "Select your style ",
        "style_definition": formatter.get_style_defs(),
        "style": session['style'],
        "all_styles": list(get_all_styles()),
        "style_bg_color": formatter.style.background_color,
        "highlighted_code": highlight(
            session['code'], Python3Lexer(), formatter
            ),
    }
    return render_template('style_selection.html', **context)

@app.route('/save_style', methods=['POST'])
def save_style():
    if request.form.get('style'):
        session['style'] = request.form.get('style')
    if request.form.get('code'):
        session['code'] = request.form.get('code')
    return redirect(url_for('style'))

@app.route('/image', methods=['GET'])
def image():
    session_data = {
        "name": app.config['SESSION_COOKIE_NAME'],
        "value": request.cookies.get(app.config['SESSION_COOKIE_NAME']),
        "url": request.host_url,
    }
    
    target_url = request.host_url + url_for('style')
    image_bytes = take_screenshot_from_url(target_url, session_data)
    context = {
        "message": "Done! ✅",
        "image_b64": base64.b64encode(image_bytes).decode('utf-8'),
    }
    return render_template('image.html', **context)

@app.route('/save_code', methods=['POST'])
def save_code():
    session['code'] = request.form.get('code') or NO_CODE_MESSAGE
    return redirect(url_for('code'))

@app.route('/reset_session', methods=['POST'])
def reset_session():
    session.clear()
    session['code'] = PLACEHOLDER
    return redirect(url_for('code'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)