from flask import Flask, url_for, request, redirect, render_template
import base64
import boto3
import json


application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = 'upload/'

@application.route('/')
def hello_world():
   return render_template('index.html')
   
@application.route('/index')
def index():
   return render_template('index.html')

@application.route('/upload_page',  methods = ['GET', 'POST'])
def upload_page():
   return render_template('upload_page.html')

# detect the celebrities
@application.route('/uploader', methods = ['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        file = request.files['file']
        bucket = 'cloud-computing-706-image-analysis'
    
        # create a resource of S3 to use 'Bucket' attribute
        s3_resource = boto3.resource('s3')

        # upload the file as on object using put_object
        s3_resource.Bucket(bucket).put_object(Key=file.filename, Body=file)
        
         # Celebrity Recognition by AWS Rekognition
        client=boto3.client('rekognition', region_name = 'us-east-2')
        response = client.recognize_celebrities(Image = {'S3Object': {'Bucket': bucket, 'Name': file.filename}})
        
        for celebrity in response['CelebrityFaces']:
            name = celebrity['Name']
            link = "#"
            if len(celebrity['Urls']) > 0:
                link = celebrity['Urls'][0]
                if not link.startswith('https://'):
                    link = 'https://' + link
        return render_template('result_page.html', tx=name, wiki=link)
    
if __name__ == "__main__":
    application.debug = True
    application.run(port = 8080, host = '0.0.0.0')
