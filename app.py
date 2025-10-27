import os,time,json,requests
from flask import Flask,render_template,jsonify
from pathlib import Path
app=Flask(__name__)
YT_API_KEY=os.environ.get('YT_API_KEY')
YT_CHANNEL_ID=os.environ.get('YT_CHANNEL_ID')
CACHE=Path('shorts_cache.json')
INTERVAL=86400
playlist=[
    {"title": "Tu | Pranay Bahuguna", "video_id": "fX6YuwEm-Ds"},
    {"title": "BAARI | Cover by Pranay Bahuguna", "video_id": "6-RTKt_oLng"},
    {"title": "Saathiya | Cover by Pranay Bahuguna", "video_id": "2C08Ei4qcoE"},
    {"title": "Samjhote | Pranay Bahuguna", "video_id": "bhe41KNDnfk"},
    {"title": "Zahir Kare | Pranay Bahuguna", "video_id": "hJKvkdN40ZU"},
    {"title": "Tum Hi Humaare | Pranay Bahuguna", "video_id": "RZK9e3E-xoY"},
    {"title": "Ek Onkar | Pranay Bahuguna", "video_id": "S5wR8K-woVg"},
    {"title": "Main Hoon Tera | Pranay Bahuguna", "video_id": "u28GZsk4LRY"},
    {"title": "Beinteha | Pranay Bahuguna", "video_id": "5J7QsC3xcKQ"},
    {"title": "Har Gali Mein Baatein Uski | Pranay Bahuguna", "video_id": "4DfhhGB4NNw"},
    {"title": "Saaye | Pranay Bahuguna", "video_id": "o03lO_yLrUE"},
    {"title": "Kuch Kaho Na | Pranay Bahuguna", "video_id": "ZPs_RNQSldU"},
    {"title": "Bheegi Bheegi Raaton Mai | Mashup ft. Varsha Tripathi", "video_id": "DnIIc-hP6I4"},
    {"title": "Deewana Hua Badal | Phir Le Aaya Dil | Mashup", "video_id": "Qdaz-Cedy3Q"},
    {"title": "Deewana Tera   | Cover by Pranay Bahuguna", "video_id": "_ARinLzJMNM"},
    {"title": "Sach Keh Raha Hai Deewana   | Cover by Pranay Bahuguna", "video_id": "OeV6tip6-gM"},
    {"title": "90s Bollywood Love | Mashup", "video_id": "ftnQwV3P0eA"}
    ]
@app.route('/') 
def home(): return render_template('index.html', songs=playlist)
def fetch_shorts():
    if not YT_API_KEY or not YT_CHANNEL_ID: return []
    url='https://www.googleapis.com/youtube/v3/search'
    params={'part':'snippet','channelId':YT_CHANNEL_ID,'maxResults':9,'order':'date','type':'video','videoDuration':'short','key':YT_API_KEY}
    r=requests.get(url,params=params,timeout=10)
    if not r.ok: return []
    items=[]
    for it in r.json().get('items',[]):
        vid=it['id'].get('videoId')
        sn=it.get('snippet',{})
        thumb=(sn.get('thumbnails') or {}).get('high',{}).get('url') or (sn.get('thumbnails') or {}).get('default',{}).get('url')
        items.append({'title':sn.get('title'),'videoId':vid,'thumbnail':thumb,'publishedAt':sn.get('publishedAt')})
    return items
def get_shorts():
    now=time.time()
    if CACHE.exists():
        try:
            data=json.loads(CACHE.read_text(encoding='utf-8'))
            if now-data.get('timestamp',0) < INTERVAL and data.get('items'): return data['items']
        except: pass
    items=fetch_shorts()
    try:
        CACHE.write_text(json.dumps({'timestamp':now,'items':items}),encoding='utf-8')
    except: pass
    return items
@app.route('/api/shorts')
def api_shorts():
    return jsonify({'items': get_shorts()})
if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
    
    # Vercel requires this
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
