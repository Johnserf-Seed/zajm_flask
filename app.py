#%%
# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
import time,os,sqlite3
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

DATABASE = '1211.sqlite'

app = Flask(__name__, instance_relative_config=True)    #工厂模式

app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

#ip限频
#limiter = Limiter(
#    app,
#    key_func=get_remote_address,   #根据访问者的IP记录访问次数
#    default_limits=["200 per day", "20 per hour"]  #默认限制，一天最多访问200次，一小时最多访问50次
#)


#防止中文被转义
app.config['JSON_AS_ASCII'] = False

test_config=None
if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

#首页
@app.route('/')
#@limiter.limit("20 per hour")  #自定义访问速率
def index():
    return render_template("userProfile2.html")
    #return '<h1>Hello,World!</h1>' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


#测试例子：姓名
#@app.route('/name', methods=('GET','POST'))
#@limiter.limit("1 per day")  #自定义访问速率
#def get_name():
#    if request.method == 'POST':
#        return '<h1>拒绝访问</h1>'
#    else:
#        return '<h1>拒绝访问</h1>'

#排名
@app.route('/ranks', methods=('GET','POST'))
#@limiter.limit("50 per hour")  #自定义访问速率
def ranking():
    #page = 1
    #page = request.args.get('page','') * 10
    #sql = ('SELECT * from  data  group by 学号 order by 次数 desc limit %d' % page)
    sql = 'SELECT * from  data  group by 学号 order by 次数 desc limit 10'
    sqliteDB = sqlite3.connect(DATABASE)
    ranks = ''
    cur = sqliteDB.execute(sql)
    ranks = cur.fetchall()
    #for row in cur.fetchall():
    #    ranks = str(row)
    print(ranks)
    return jsonify(ranks)

#排名
@app.route('/rank', methods=('GET','POST'))
#@limiter.limit("50 per hour")  #自定义访问速率
def rank():
    page = request.args.get('page','')
    page_index = (int(page)-1) * 10
    page = int(page) * 10
    #sql = ('SELECT * from  data  group by 学号 order by 次数 desc limit %d' % page)
    sql = 'SELECT * from  data  group by 学号 order by 次数 desc limit '+ str(page_index) + ',' + str('10')
    print(sql)
    sqliteDB = sqlite3.connect(DATABASE)
    ranks = ''
    cur = sqliteDB.execute(sql)
    ranks = cur.fetchall()
    #for row in cur.fetchall():
    #    ranks = str(row)
    print(ranks)
    return jsonify(ranks)


#用户数据
@app.route('/userProfile', methods=('GET','POST'))
#@limiter.limit("20 per hour")  #自定义访问速率
def get_profile():
    name = request.args.get('name','')
    number = request.args.get('number','')
    print(name,number)

    #data = ['and','like','exec','insert','select','drop','grant','alter','delete','update','count','chr','mid','master','truncate','char','delclare','or','\b','(\*',';']
    #for v in data:
    #    if number == v or name == v:
    #        return 'error!'

    if name == '':
        sql = ("SELECT * FROM data WHERE 学号 = %s" % (number))
    if number == '':
        sql = ("SELECT * FROM data WHERE 姓名 = '%s'" % (name))

    try:
        description = "“早安经贸 不负晨光”晨间锻炼次数查询表（截至2022.12.11）"
        sqliteDB = sqlite3.connect(DATABASE)
        print(sql)
        #sql查询
        cur = sqliteDB.execute(sql)
        for row in cur.fetchall():
            number = str(row[0])
            u_name = str(row[1])
            classes = str(row[2])
            counts = str(row[3])
            college = str(row[4])
        sqliteDB.close()
        return {'now_time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) , 'class':classes ,'name':u_name,\
            'counts':counts,'college':college,'number':number,'state_code':'200'\
                ,'description':description}
    except Exception:
        return {'now_time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) , 'class':'' ,'name':'',\
            'counts':'','college':'','number':'','state_code':'-1'\
                ,'description':description}


if __name__ == "__main__":
    app.run()
    # app.run(debug=True,ssl_context=('cn-cd-dx-4.natfrp.cloud+4.pem', 'cn-cd-dx-4.natfrp.cloud+4-key.pem'),host='127.0.0.1',port=5000)

