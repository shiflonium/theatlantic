from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import models
from werkzeug.utils import secure_filename
from datetime import datetime


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(filename)

        with open(filename, 'r') as fp:
            content = fp.readlines()

        content = [line.strip().split('\t') for line in content]

        for line in content:
            # map columns to names
            customer_id = int(line[0])
            first_name = line[1]
            last_name = line[2]
            address = line[3]
            state = line[4]
            zip_code = line[5]
            status = line[6]
            product_id = int(line[7])
            product_name = line[8]
            price = line[9]
            date = datetime.strptime(line[10], '%Y-%m-%dT%H:%MZ')
            #check if customer in database
            customer = db.session.query(models.Customer).filter(models.Customer.id == customer_id).first()
            if not customer:
                c = models.Customer(
                    customer_id,
                    first_name,
                    last_name,
                    address,
                    state,
                    zip_code
                )
                db.session.add(c)
            else:
                if customer.address != line[3] or customer.address != state or customer.zip != zip_code:

                    customer.address = address
                    customer.state = state
                    customer.zip = zip_code

                    db.session.commit()


            # check if product in db
            product = db.session.query(models.Product).filter(models.Product.id == product_id).first()
            if not product:
                p = models.Product(
                    product_id,
                    product_name
                )
                db.session.add(p)

            # process order data
            if status == 'canceled':
                o = db.session.query(models.Order).filter(
                    models.Order.customer_id == customer_id,
                    models.Order.product_id == product_id
                ).first()

                if o: # if the order is already in the db
                    if o.status == 'new' and o.date < date: # if the status of the order is new and was placed before
                        o.status = status
                        db.session.commit()

                else:
                    errors.append('Order of product {p_name} does not exist for customer {c_name}'.format(
                        p_name=product_name, c_name=first_name + ' ' + last_name)
                    )

            else: # the order did not exist in the db, we will add this to the list of errors
                new_order = models.Order(
                    customer_id,
                    product_id,
                    price,
                    status,
                    date
                )
                db.session.add(new_order)

        db.session.commit()

    return render_template('index.html', errors=errors)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


