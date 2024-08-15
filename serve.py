from app import *

@app.route('/')
def index():
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)