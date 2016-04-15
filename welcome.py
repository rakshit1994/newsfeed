# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os,json
from flask import Flask, jsonify, render_template, redirect, url_for, request
from urllib import urlopen
import plotly
plotly.tools.set_credentials_file(username='RakshitSingh', api_key=_YOUR API KEY_)
import plotly.plotly as py
import plotly.graph_objs as go


app = Flask(__name__)
count = 0

@app.route('/')
def Welcome():
    return render_template('index.html')

@app.route('/myapp')
def WelcomeToMyapp():
    return render_template('myapp.html')


@app.route('/news',methods = ['GET','POST'])
def GetFeed():
    error = None
    if request.method == 'POST':
        if request.form['search']:
            searchfield = request.form['search']
            cnt = request.form['cnt']
            print searchfield
        #request.form['title'] = searchfield
            url = 'https://access.alchemyapi.com/calls/data/GetNews?apikey=_YOUR API KEY_&return=enriched.url.title,enriched.url.enrichedTitle.docSentiment,enriched.url.enrichedTitle.taxonomy&start=1459209600&end=1459897200&q.enriched.url.enrichedTitle.entities.entity=|text=%s,type=person|&count=%s&outputMode=json'%(searchfield,cnt)
            url = urlopen(url).read()
            #print url
            result = json.loads(url)
            i=0
            x=[]
            y=[]
            for w in result['result']['docs']:
                x.append(result['result']['docs'][i]['source']['enriched']['url']['enrichedTitle']['docSentiment']['type'])
                y.append(result['result']['docs'][i]['source']['enriched']['url']['title'])
                i+=1
        count = i 
        p= 0
        nu= 0
        n= 0
        for sent in x:
            if(sent == "positive"):
                p+=1
            if(sent == "neutral"):
                nu+=1
            if(sent == "negative"):
                n+=1
        z=[p,nu,n]
        data = [go.Bar(x=['positive', 'neutral', 'negative'],y=z)]
        plot_url = str(py.plot(data, filename='basic-bar'))
        plot_png = str(plot_url)+'.png'

        return render_template('myapp.html',paragraph=x,paragraph2=y,count=count,plot_url=plot_url,plot_png=plot_png)
    return render_template('news.html')


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port),debug=True)
