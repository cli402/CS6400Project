
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash,send_from_directory,jsonify

import image
import blockhash,os,imagehash,json
from werkzeug import secure_filename

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','py'])


# DATABASE = '/tmp/img.db'
# DEBUG = True
# SECRET_KEY = 'development key'
# USERNAME = 'admin'
# PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/content/",methods=['GET','POST'])
def content():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            ##calculate the hash value of the pic
            hash_val = image.cal_hash_val(file_path)
            #insert into the database 
            if not image.pic_exist(hash_val[2]):
                image.insert_image(hash_val[0],hash_val[1],hash_val[2],file_path)
            x = image.get_format(image.hamming(hash_val[0],hash_val[2]))
            print x
            return render_template('retrieval.html',filename=x)
    else:
        return render_template('retrieval.html')


@app.route("/upload",methods =['GET','POST'])
def upload():
    if request.method =="POST":
        file  = request.files['file']
        #if file and allowed_file(file.filename):
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print file_path
            x= '../'+file_path
            print x
            #calculate the hash value of the pic
            hash_val = image.cal_hash_val(file_path)
            if not image.pic_exist(hash_val[2]):
                 image.insert_image(hash_val[0],hash_val[1],hash_val[2],x)
            return render_template('upload.html',filename = x,phash = hash_val[2])
        tag = request.form['tag_name']
        print tag
        if tag :
            tag=tag.split(',')
            for item in tag:
                print item
                if not image.tag_exist(item,request.form['phash']):
                    image.insert_tags(item,request.form['phash'])
            return render_template('upload.html',success=True)
    else:
        return render_template('upload.html')



@app.route("/upload_tag",methods =['GET','POST'])
def upload_tag():
    if request.method =="POST":
        tag = request.form['tag_name']
        print tag
        if tag :
            tag=tag.split(',')
            for item in tag:

                image.insert_tags(item,request.form['phash'])
            return render_template('upload_tag.html',success=1)
    else:
        return render_template('upload_tag.html',keys=request.args.get('filename'), obj=request.args.get('phash'))


@app.route("/tag",methods=['GET','POST'])
def tag():
    if request.method == 'POST':
            textline  = request.form['textline']
            print textline
            tag_pics = image.get_location_by_tag(textline)
            print tag_pics
            pic_exist = True 
            if len(tag_pics) == 0:
                pic_exist = False
            print pic_exist
            return render_template('tag.html',pic_exist = pic_exist,tagname=tag_pics,request_name = textline)
    else:
        return render_template('tag.html')



@app.route("/report",methods=['GET','POST'])
def report():
    if request.method == 'POST':        
            return render_template('upload.html',filename=x)
    else:
        return render_template('retrieval.html')

#NAMES=["name","dog","come","ab","abd","ZHAODATUI"]


@app.route('/autocomplete',methods=['GET'])
def autocomplete():
    search = request.args.get('term')
    #app.logger.debug(search)
    NAMES = image.auto_complete()
    return jsonify(json_list=NAMES) 







###############helper function################
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



if __name__ == "__main__":
    #todo: toggle debug from config
    app.debug = True
    app.run()