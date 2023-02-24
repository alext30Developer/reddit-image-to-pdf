import os
import urllib.request
import praw
import img2pdf
from PyPDF2 import PdfMerger

print("Scraping 500 Hot posts and picking only the images from r/Memes...")

reddit = praw.Reddit(client_id='your_client_id',
                     client_secret='your_client_secret',
                     user_agent='anything')

if not os.path.exists('images'):
    os.makedirs('images')

subreddit = reddit.subreddit('memes')
top_posts = subreddit.hot(limit=500)

for post in top_posts:
    if post.url.endswith('.jpg') or post.url.endswith('.png'):
        urllib.request.urlretrieve(post.url, os.path.join('images', f"{post.id}.jpg"))
        print(f"Downloaded {post.id}.jpg")

print("Converting images to PDF...")

if not os.path.exists("pdfs"):
    os.mkdir("pdfs")

for filename in os.listdir("images"):
    if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
        with open(os.path.join("images", filename), "rb") as f:
            image = f.read()
        pdf_bytes = img2pdf.convert(image)
        with open(os.path.join("pdfs", os.path.splitext(filename)[0] + ".pdf"), "wb") as f:
            f.write(pdf_bytes)

print("Merging PDF files into one...")

merger = PdfMerger()

for filename in os.listdir("pdfs"):
    if filename.endswith(".pdf"):
        merger.append(os.path.join("pdfs", filename))
with open("output.pdf", "wb") as f:
    merger.write(f)

print("Merged PDF file saved as output.pdf")
