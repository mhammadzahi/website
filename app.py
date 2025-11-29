from flask import Flask, render_template, request, jsonify
from functions.helpers import slugify
from functions.database import get_db

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


# @app.route('/api/post/<path:post_slug>/title')
# def post_title_api(post_slug):
#     """Return the post title as JSON for a given post ID.

#     Response examples:
#     - 200: {"id": 1, "title": "The Future of Smart Homes"}
#     - 404: {"error": "Post not found"}
#     """
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute("SELECT title FROM posts WHERE slug=?", (post_slug,))
#     row = cur.fetchone()
#     conn.close()
#     if row:
#         print('----------row:', row)
#         return jsonify({"slug": post_slug, "title": row['title']}), 200
#     return jsonify({"error": "Post not found"}), 404

@app.route('/api/newsletter/subscribe', methods=['POST'])
def newsletter_subscribe():
    # Here you would handle the newsletter subscription logic
    # For now, we'll just print to console
    print(f"***Email: {request.json.get('email')}")
    return jsonify({"message": "Subscription successful"}), 200

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Here we would handle the form submission (e.g., send email)
        # For now, we'll just print to console
        data = request.json
        print(f"Name: {data.get('name')}")
        print(f"Email: {data.get('email')}")
        print(f"Subject: {data.get('subject')}")
        print(f"Message: {data.get('message')}")
        return jsonify({"success": True, "message": "Message sent successfully"}), 200
    return render_template('contact.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
