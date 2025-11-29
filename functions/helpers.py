# import re


# def slugify(title: str) -> str:
#     """Create a URL-friendly slug from a post title."""
#     print(f"!!!!!Generating slug for title: {title}")
#     slug = title.lower()
#     slug = re.sub(r"[^a-z0-9\s-]", "", slug)
#     slug = re.sub(r"[\s_-]+", "-", slug)
#     slug = slug.strip('-')
#     return slug
