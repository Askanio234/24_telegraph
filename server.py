import os
from flask import Flask, render_template, request, redirect, url_for, abort
from sqlalchemy import exc
from db_schema import db_session, Posts
from generate_slug import random_slug

SLUG_LENGTH = 10

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template('form.html', show_button=True,
                                header="", signature="", body="")
    if request.method == 'POST':
        try:
            post_slug = random_slug(SLUG_LENGTH) 
            post_to_add = Posts(post_url=post_slug,
                                post_header=request.form['header'],
                                post_signature=request.form['signature'],
                                post_body=request.form['body'])
            db_session.add(post_to_add)
            db_session.commit()
            return redirect(url_for('posts_by_slug', post_slug=post_slug))
        except exc.IntegrityError:
            db_session.rollback()
            abort(500)


@app.route('/posts/<post_slug>')
def posts_by_slug(post_slug):
    post_to_show = db_session.query(Posts).filter(
                                        Posts.post_url == post_slug
                                        ).first()
    if post_to_show is not None:
        return render_template('form.html', show_button=False,
                                disabled=True,
                                header=post_to_show.post_header,
                                signature=post_to_show.post_signature,
                                body=post_to_show.post_body)
    else:
        abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
