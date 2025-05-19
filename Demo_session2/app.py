from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory data stores
restaurants = [
    {'id': 1, 'name': 'The Gourmet Kitchen', 'description': 'Fine dining with a modern twist.', 'image': 'gourmet.jpg'},
    {'id': 2, 'name': 'Pizza Palace', 'description': 'Authentic Italian pizza and more.', 'image': 'pizza.jpg'},
    {'id': 3, 'name': 'Sushi World', 'description': 'Fresh sushi and sashimi.', 'image': 'sushi.jpg'}
]  # List of dicts: {id, name, description}
reviews = []      # List of dicts: {restaurant_id, rating, comment, factors}

@app.route('/')
def index():
    # Calculate average rating for each restaurant
    restaurant_ratings = {}
    for r in restaurants:
        r_reviews = [rev for rev in reviews if rev['restaurant_id'] == r['id']]
        if r_reviews:
            avg = sum([rev['rating'] for rev in r_reviews]) / len(r_reviews)
            restaurant_ratings[r['id']] = round(avg, 2)
        else:
            restaurant_ratings[r['id']] = None
    return render_template('index.html', restaurants=restaurants, restaurant_ratings=restaurant_ratings)

@app.route('/add', methods=['GET', 'POST'])
def add_restaurant():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image = request.form.get('image', 'gourmet.jpg')
        restaurant_id = len(restaurants) + 1
        restaurants.append({'id': restaurant_id, 'name': name, 'description': description, 'image': image})
        return redirect(url_for('index'))
    return render_template('add_restaurant.html')

@app.route('/restaurant/<int:restaurant_id>')
def view_restaurant(restaurant_id):
    restaurant = next((r for r in restaurants if r['id'] == restaurant_id), None)
    restaurant_reviews = [rev for rev in reviews if rev['restaurant_id'] == restaurant_id]
    return render_template('view_restaurant.html', restaurant=restaurant, reviews=restaurant_reviews)

@app.route('/restaurant/<int:restaurant_id>/rate', methods=['GET', 'POST'])
def rate_restaurant(restaurant_id):
    restaurant = next((r for r in restaurants if r['id'] == restaurant_id), None)
    if not restaurant:
        return redirect(url_for('index'))
    if request.method == 'POST':
        rating = int(request.form['rating'])
        comment = request.form['comment']
        factors = request.form['factors']
        reviews.append({'restaurant_id': restaurant_id, 'rating': rating, 'comment': comment, 'factors': factors})
        return redirect(url_for('view_restaurant', restaurant_id=restaurant_id))
    return render_template('rate_restaurant.html', restaurant=restaurant)

if __name__ == '__main__':
    app.run(debug=True)
