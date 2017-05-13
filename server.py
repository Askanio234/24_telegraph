import datetime
import os
from flask import Flask, render_template, request, redirect, url_for, abort
from sqlalchemy import exc
from db_schema import db_session, Posts


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template('form.html', show_button=True,
                                header="", signature="", body="")
    if request.method == 'POST':
        try:
            post_id = '{}-{}'.format(
                                request.form['header'].replace(" ","-"),
                                str(datetime.date.today()))  
            post_to_add = Posts(post_url=post_id,
                                post_header=request.form['header'],
                                post_signature=request.form['signature'],
                                post_body=request.form['body'])
            db_session.add(post_to_add)
            db_session.commit()
            return redirect(url_for('posts_by_id', post_id=post_id))
        except exc.IntegrityError:
            db_session.rollback()
            return "Something went very bad, try again later"


@app.route('/posts/<post_id>')
def posts_by_id(post_id):
    post_to_show = db_session.query(Posts).filter(
                                        Posts.post_url == post_id
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

# host='0.0.0.0'
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
