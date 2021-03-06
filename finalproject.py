from flask import Flask, render_template, request, url_for, redirect, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurant/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        restaurantName = request.form['name']
        if restaurantName:
            newRestaurant = Restaurant(name=restaurantName)
            session.add(newRestaurant)
            session.commit()
            return redirect(url_for('showRestaurants'))
        else:
            return render_template('newrestaurant.html')    
    else:
        return render_template('newrestaurant.html')
        

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
    if restaurant == None:
        abort(404)
    if request.method == 'POST':
        restaurantName = request.form['name']
        if restaurantName:
            restaurant.name = restaurantName
            session.add(restaurant)
            session.commit()
            return redirect(url_for('showRestaurants'))
        else:
            return render_template('editrestaurant.html', restaurant=restaurant)     
    else:
        return render_template('editrestaurant.html', restaurant=restaurant) 

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
    if restaurant == None:
        abort(404)
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleterestaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
    if restaurant == None:
        abort(404)
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        course = request.form['course']
        if name:
            newMenuItem = MenuItem(
                name=name,
                description=description,
                price=price,
                course=course,
                restaurant_id=restaurant_id)
            session.add(newMenuItem)
            session.commit()
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
        else:
            return render_template('newmenuitem.html', restaurant_id=restaurant_id)    
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one_or_none()
    if item == None:
        abort(404)
    if request.method == 'POST':
        itemName = request.form['name']
        if itemName:
            item.name = itemName
            session.add(item)
            session.commit()
            return redirect(url_for('showMenu', restaurant_id=item.restaurant_id))
        else:
            return render_template('editmenuitem.html', item=item)
    else:
        return render_template('editmenuitem.html', item=item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id, id=menu_id).one_or_none()
    if item == None:
        abort(404)
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=item.restaurant_id))
    else:
        return render_template('deletemenuitem.html', item=item)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)
