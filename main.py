from flask import Flask
from flask import render_template, redirect
from data.db_session import create_session, global_init
from data.users import User
from data.jobs import Jobs
import json

app = Flask(__name__)
db_name = 'mars_explorer.db'
global_init(db_name)
db_sess = create_session()
jobs = []
for job in db_sess.query(Jobs).all():
    user = db_sess.query(User).filter(User.id == job.team_leader).first()
    name = user.surname + ' ' + user.name
    is_finished = 'Is finished' if job.is_finished else 'Is not finished'
    jobs.append({"id": job.id, "title": job.job, "team_leader": name, "duration": job.work_size, "collaborators": job.collaborators, "is_finished": is_finished})
with open('jobs.json', 'w') as f:
    json.dump(jobs, f, indent=2)

@app.route('/')
def jobs(title=''):
    with open('jobs.json', encoding="utf8") as f:
        data = json.loads(f.read())
    return render_template('jobs.html',
                           h1title='Миссия Колонизация Марса',
                           h4title='И на Марсе будут яблони цвести!',
                           jobs=data)




if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
