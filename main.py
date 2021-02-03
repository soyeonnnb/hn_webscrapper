import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"

db = {}
detailDb = {}

app = Flask("DayNine")

popular_data =  requests.get(popular).json()['hits']
new_data =  requests.get(new).json()['hits']

def article_sort(order_by):
  if order_by == "new":
    data = new_data
  elif order_by == "popular":
    data= popular_data
  else:
    data=popular_data
  articles = []
  for article in data:
    article_id = article['objectID']
    existingArticle = db.get(article_id)
    if existingArticle:
      art = existingArticle
    else:
      title = article['title']
      url = article['url']
      points = article['points']
      author = article['author']
      comments = article['num_comments']
      art = {
      'title':title,
      'url':url,
      'points':points,
      'author':author,
      'comments':comments,
      'id':article_id
      }
      db[article_id] = art
    articles.append(art)
    art={}
  return articles

@app.route("/")
def home():
  order_by = request.args.get('order_by')
  articles = article_sort(order_by)
  return  render_template("index.html", articles = articles, order_by = order_by)

@app.route("/<id>")
def detail_sort(id):
  url = make_detail_url(id)
  detail_data = requests.get(url).json()
  title = detail_data['title']
  points = detail_data['points']
  detail_author = detail_data['author']
  detail_url = detail_data['url']
  print(title, points, detail_author, detail_url)
  detail_comments = detail_data['children']
  comments=[]
  for ob in detail_comments:
    text = ob['text']
    url = ob['url']
    author = ob['author']
    comment = {
      'text':text,
      'url':url,
      'author':author
    }
    comments.append(comment)
    comment={}
  return render_template("detail.html", title=title, points=points, detail_author=detail_author, detail_url=detail_url, comments=comments)
  

app.run(host="0.0.0.0")