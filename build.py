"""
Build script: converts blog/posts/*.md -> blog/html/*.html
and regenerates blog/index.html with a list of all posts.

Usage:
    python build.py

Requires:
    pip install markdown
"""

import os
import re
import markdown
from datetime import date

POSTS_DIR = "blog/posts"
HTML_DIR = "blog/html"
BLOG_INDEX = "blog/index.html"


def slugify(filename):
    return filename.replace(".md", "")


def parse_frontmatter(text):
    """Extract optional title and date from top of markdown file.

    Expected format at top of .md file (optional):
        # Post Title
        date: 2026-04-12
    """
    title = None
    post_date = None

    lines = text.strip().splitlines()

    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()

    for line in lines[:5]:
        match = re.match(r"^date:\s*(\d{4}-\d{2}-\d{2})", line)
        if match:
            post_date = match.group(1)

    return title, post_date


def post_template(title, post_date, content_html):
    date_html = f'<p class="post-date">{post_date}</p>' if post_date else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — Natalie Gable</title>
  <link rel="stylesheet" href="../../style.css" />
  <link rel="icon" href="../../favicon.ico" />
</head>
<body>

  <header>
    <nav>
      <a href="../../index.html">About</a>
      <a href="../../blog/index.html">Blog</a>
    </nav>
  </header>

  <main>
    <article class="post">
      <h1>{title}</h1>
      {date_html}
      {content_html}
    </article>
  </main>

  <footer>
    <p>&copy; 2026 Natalie Gable</p>
  </footer>

</body>
</html>
"""


def blog_index_template(posts):
    items = ""
    for slug, title, post_date in posts:
        date_str = f'<span class="post-date">{post_date}</span>' if post_date else ""
        items += f"""
        <li>
          {date_str}
          <a href="html/{slug}.html">{title}</a>
        </li>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Blog — Natalie Gable</title>
  <link rel="stylesheet" href="../style.css" />
  <link rel="icon" href="../favicon.ico" />
</head>
<body>

  <header>
    <nav>
      <a href="../index.html">About</a>
      <a href="../blog/index.html">Blog</a>
    </nav>
  </header>

  <main>
    <section>
      <h2>Blog</h2>
      <ul class="post-list">
        {items}
      </ul>
    </section>
  </main>

  <footer>
    <p>&copy; 2026 Natalie Gable</p>
  </footer>

</body>
</html>
"""


def build():
    os.makedirs(HTML_DIR, exist_ok=True)
    posts = []

    md_files = sorted(
        [f for f in os.listdir(POSTS_DIR) if f.endswith(".md")], reverse=True
    )

    for filename in md_files:
        slug = slugify(filename)
        filepath = os.path.join(POSTS_DIR, filename)

        with open(filepath, "r") as f:
            text = f.read()

        title, post_date = parse_frontmatter(text)
        if not title:
            title = slug.replace("-", " ").title()

        content_html = markdown.markdown(text, extensions=["fenced_code", "tables"])

        html = post_template(title, post_date, content_html)
        out_path = os.path.join(HTML_DIR, f"{slug}.html")
        with open(out_path, "w") as f:
            f.write(html)

        posts.append((slug, title, post_date))
        print(f"Built: {out_path}")

    index_html = blog_index_template(posts)
    with open(BLOG_INDEX, "w") as f:
        f.write(index_html)
    print(f"Built: {BLOG_INDEX}")


if __name__ == "__main__":
    build()