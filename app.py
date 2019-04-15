from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import models
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(filename)

        with open(filename, 'r') as fp:
            content = fp.readlines()

        content = [line.strip().split('\t') for line in content]

        for line in content:
            customer_id = int(line[0])
            #check if customer in database
            customer = db.session.query(models.Customer).filter(models.Customer.id == customer_id).first()
            if not customer:
                print(111)
            else:
                print(2222)




    return render_template('templates.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


