from flask import Flask, render_template, request
import dashapp
import dash

server = Flask(__name__)
app = dash.Dash(__name__, server=server, url_base_pathname='/dashapp')

@app.route('/')
def index():
    return 'Welcome!'

@app.route('/dash')
def dash_chart():
    return flask.redirect('/dashapp') #Put the dash app here, so that it's the home page
                                         #Data navbar link will use this route also
# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html') # This can be the about page

if __name__ == '__main__':
    app.run(debug=True)
