from flask import Flask,render_template,request,jsonify,abort
from complex_loci import *

from views.matrix import matrix_blueprint

app=Flask(__name__)
app.register_blueprint(matrix_blueprint)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/loci-plotter')
def loci():
    return render_template('loci.html')

@app.route('/_plot')
def plot():
    eq=request.args.get('eq',0,type=str)
    try:
        LHS,RHS=eq.split('=')
        line=get_implicit(LHS,RHS,latx=True)
        repr(line)
        print(line)
        return jsonify(result=line)
    except:
        abort(500)

@app.route('/operations-argand')
def operations():
    return render_template('operations.html')

@app.route('/ttt')
def ttt():
    return render_template('ttt.html')

if __name__=='__main__':
    app.debug = True
    app.run()
