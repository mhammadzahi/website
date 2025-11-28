import sqlite3
import os
from typing import List, Dict
from .helpers import slugify


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'posts.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        date TEXT,
        author TEXT,
        content TEXT,
        image TEXT,
        slug TEXT UNIQUE
    )
    """)
    conn.commit()
    conn.close()


def seed_db(seed_posts: List[Dict]):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(1) FROM posts")
    count = cur.fetchone()[0]
    if count == 0:
        seen_slugs = set()
        for p in seed_posts:
            title = p.get('title', '')
            base = slugify(title)
            slug = base or 'post'
            suffix = 1
            # ensure slug uniqueness in DB and in this run
            while True:
                cur.execute("SELECT 1 FROM posts WHERE slug=?", (slug,))
                if not cur.fetchone() and slug not in seen_slugs:
                    break
                suffix += 1
                slug = f"{base}-{suffix}"
            seen_slugs.add(slug)
            if p.get('id'):
                cur.execute(
                    "INSERT OR IGNORE INTO posts (id, title, date, author, content, image, slug) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (p['id'], p['title'], p.get('date'), p.get('author'), p.get('content'), p.get('image'), slug)
                )
            else:
                cur.execute(
                    "INSERT OR IGNORE INTO posts (title, date, author, content, image, slug) VALUES (?, ?, ?, ?, ?, ?)",
                    (p['title'], p.get('date'), p.get('author'), p.get('content'), p.get('image'), slug)
                )
        conn.commit()
    conn.close()


# Default seed data moved here so `app.py` can stay small and import the constant
SEED_POSTS: List[Dict] = [
    {
        'id': 1,
        'title': 'The Future of Smart Homes',
        'date': 'November 28, 2025',
        'author': 'Sarah Connor',
        'content': 'Smart homes are becoming more intuitive. With the rise of AI and IoT, our living spaces are learning from our habits...',
        'image': 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=800&q=80'
    },
    {
        'id': 2,
        'title': 'Industrial IoT Revolution',
        'date': 'November 25, 2025',
        'author': 'John Smith',
        'content': 'Industry 4.0 is here. Factories are becoming smarter, more efficient, and safer thanks to connected sensors...',
        'image': 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=800&q=80'
    },
    {
        'id': 3,
        'title': 'IoT Security Best Practices bb',
        'date': 'November 20, 2025',
        'author': 'Emily Chen',
        'content': 'As we connect more devices, security becomes paramount. Here are the top 5 tips to secure your IoT ecosystem...',
        'image': 'https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=800&q=80'
    }
]
