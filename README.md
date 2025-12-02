# YallaIoT Website

A professional Flask-based website for YallaIoT, featuring a blog system, contact management, and newsletter subscription functionality.

## 🚀 Features

- **Dynamic Blog System**: Paginated blog posts with individual post pages
- **Newsletter Subscription**: Email collection system for newsletter subscribers
- **Contact Management**: Contact form with message storage in SQLite database
- **SEO Optimized**: Built-in sitemap.xml and robots.txt for search engine optimization
- **Responsive Design**: Modern, mobile-friendly interface
- **Error Handling**: Custom 404 error pages

## 📋 Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- SQLite3

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mhammadzahi/website.git
   cd website
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   
   Ensure you have a `database.db` file with the following tables:
   - `posts` (id, slug, title, content, created_at, etc.)
   - `newsletter_subscribers` (id, email, created_at)
   - `contact_messages` (id, full_name, email_address, subject, message, created_at)

## 🚀 Running the Application

### Development Mode

```bash
python app.py
```

The application will run on `http://localhost:5000` with debug mode enabled.

### Production Mode with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Options:
- `-w 4`: Number of worker processes (adjust based on CPU cores)
- `-b 0.0.0.0:5000`: Bind to all interfaces on port 5000
- `--access-logfile -`: Log access requests to stdout
- `--error-logfile -`: Log errors to stdout

**Recommended production command:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile - --error-logfile - app:app
```

## 📁 Project Structure

```
website/
├── app.py                  # Main Flask application
├── database.db             # SQLite database
├── requirements.txt        # Python dependencies
├── robots.txt             # Search engine crawler rules
├── functions/
│   └── database.py        # Database operations
├── static/
│   ├── css/
│   │   └── style.css      # Stylesheets
│   ├── img/               # Images and media
│   └── js/
│       └── script.js      # JavaScript files
└── templates/
    ├── base.html          # Base template
    ├── index.html         # Homepage
    ├── about.html         # About page
    ├── services.html      # Services page
    ├── blog.html          # Blog listing page
    ├── post.html          # Individual post page
    ├── contact.html       # Contact page
    ├── terms.html         # Terms and conditions
    └── 404.html           # Error page
```

## 🌐 API Endpoints

### Public Routes
- `GET /` - Homepage
- `GET /about` - About page
- `GET /services` - Services page
- `GET /blog` - Blog listing (paginated)
- `GET /blog/page/<int:page>` - Blog pagination
- `GET /post/<slug>` - Individual blog post
- `GET /contact` - Contact page
- `POST /contact` - Submit contact form
- `GET /terms` - Terms and conditions
- `GET /sitemap.xml` - XML sitemap for SEO
- `GET /robots.txt` - Robots.txt for search engines

### API Routes
- `POST /api/newsletter/subscribe` - Subscribe to newsletter

**Request body:**
```json
{
  "email": "user@example.com"
}
```

## 🔧 Configuration

### Database Location
The database path is configured in `functions/database.py`:
```python
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')
```

### Domain Configuration
Update the domain in the following locations:
- `app.py` - sitemap.xml generation (line ~106)
- `robots.txt` - Sitemap URL

## 🔒 Security Features

- API endpoints blocked from search engine crawling
- Static assets protection in robots.txt
- Database files excluded from public access
- Environment files protected

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is proprietary and confidential.

## 👤 Author

**Mohammad Hammadzahi**
- GitHub: [@mhammadzahi](https://github.com/mhammadzahi)
- Website: [yallaiot.com](https://www.yallaiot.com)

## 🐛 Issues

Found a bug? Please open an issue on GitHub with detailed information about the problem.

---

**Built with ❤️ using Flask**