from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dic(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary



with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random",methods = ['GET'])
def random_cafe():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    random_cafe = random.choice(cafes)
    # return jsonify(id = cafe.id,
    #                name = cafe.name,
    #                map = cafe.map_url,
    #                image = cafe.img_url,
    #                location=cafe.location,
    #                seats=cafe.seats,
    #                has_toilet=cafe.has_toilet,
    #                has_wifi=cafe.has_wifi,
    #                has_sockets=cafe.has_sockets,
    #                can_take_calls = cafe.can_take_calls,
    #                coffee_price = cafe.coffee_price
    #                )
    return jsonify(cafe = random_cafe.to_dic())

# HTTP GET - Read Record
@app.route("/all",methods = ['GET'])
def all_cafes():
    cafes_list = db.session.execute(db.select(Cafe)).scalars().all()
    cafes = []
    for cafe in cafes_list:
        cafes.append(cafe.to_dic())
    return jsonify(cafe = cafes)

@app.route("/search",methods = ['GET'])
def find_by_loc():
    error = {"Not Found": "Sorry, we don't have a cafe at that location"}
    loc = request.args.get("loc")
    cafes_list = db.session.execute(db.select(Cafe).where(Cafe.location == loc)).scalars().all()
    cafes = []
    for cafe in cafes_list:
        cafes.append(cafe.to_dic())
    if cafes == []:
        return jsonify(error = error)

    return jsonify(cafe=cafes)

# HTTP POST - Create Record
@app.route("/add",methods = ['POST'])
def add_cafe():
    cafe = Cafe(
    name = request.form.get("name"),
    map_url = request.form.get("map_url"),
    img_url = request.form.get("img_url"),
    location = request.form.get("loc"),
    has_sockets = bool(request.form.get("sockets")),
    has_toilet = bool(request.form.get("toilet")),
    has_wifi = bool(request.form.get("wifi")),
    can_take_calls = bool(request.form.get("calls")),
    seats = request.form.get("seats"),
    coffee_price = request.form.get("coffee_price"),
    )
    db.session.add(cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})




# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>",methods = ['GET','POST','PATCH'])
def update_price(cafe_id):
    cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    new_price = request.args.get("new_price")
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the coffee price."})
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})
# HTTP DELETE - Delete Record
@app.route("/delete-cafe/<int:cafe_id>",methods = ['GET','POST','PATCH','DELETE'])
def delete_cafe(cafe_id):
    api_key = request.args.get("api_key")
    cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    if api_key == "TopSecretAPIKey":
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully removed the cafe from the database."})
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})
    else:
        return jsonify({"Error": "Sorry wrong API key you are not allowed."})

if __name__ == '__main__':
    app.run(debug=True)
