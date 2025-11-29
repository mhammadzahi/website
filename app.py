from flask import Flask, render_template, request, jsonify
from functions.database import get_db, new_subscriber, new_message
# from functions.helpers import slugify

# from flask_babel import Babel
# app.config['BABEL_DEFAULT_LOCALE'] = 'en'
# app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'ar']
# babel = Babel(app)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/blog')
@app.route('/blog/page/<int:page>')
def blog(page=1):
    per_page = 9
    # Query total posts from DB
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(1) FROM posts")
    total_posts = cur.fetchone()[0]
    total_pages = (total_posts + per_page - 1) // per_page  # Ceiling division

    # Calculate offset
    start = (page - 1) * per_page

    # Get posts for current page (newest first)
    cur.execute("SELECT * FROM posts ORDER BY id DESC LIMIT ? OFFSET ?", (per_page, start))
    rows = cur.fetchall()
    paginated_posts = [dict(r) for r in rows]
    conn.close()
    
    # Calculate page range for pagination display
    page_range = []
    if total_pages <= 7:
        page_range = list(range(1, total_pages + 1))
    else:
        if page <= 4:
            page_range = list(range(1, 6)) + ['...', total_pages]
        elif page >= total_pages - 3:
            page_range = [1, '...'] + list(range(total_pages - 4, total_pages + 1))
        else:
            page_range = [1, '...'] + list(range(page - 1, page + 2)) + ['...', total_pages]
    
    return render_template('blog.html', posts=paginated_posts, page=page, total_pages=total_pages, page_range=page_range)


@app.route('/post/<path:post_slug>')
def post(post_slug):
    # Find post by slug (derived from title)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts WHERE slug=?", (post_slug,))
    row = cur.fetchone()
    post = dict(row) if row else None
    conn.close()
    return render_template('post.html', post=post)


@app.route('/api/newsletter/subscribe', methods=['POST'])
def newsletter_subscribe():
    email_address = request.json.get('email')

    if not new_subscriber(email_address):
        print("Failed to add new subscriber: ", email_address)

    return jsonify({"message": "Subscription successful"}), 200



@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        email_address = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        if not new_message(name, email_address, subject, message):
            print("Failed to save message: ", data)

        return jsonify({"success": True, "message": "Message sent successfully"}), 200

    # GET
    return render_template('contact.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
