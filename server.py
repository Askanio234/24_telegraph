import datetime
from flask import Flask, render_template, request, redirect, url_for
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
    return render_template('form.html', show_button=False,
                            header=post_to_show.post_header,
                            signature=post_to_show.post_signature,
                            body=post_to_show.post_body)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
