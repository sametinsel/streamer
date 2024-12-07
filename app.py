import requests
from flask import Flask, request
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

@app.route('/<m3u8>')
def index(m3u8):
    # URL'i düzenle
    m3u8 = request.url.replace('__', '/')
    source = m3u8.replace('https://orca-app-y5vl4.ondigitalocean.app/', '').replace('%2F', '/').replace('%3F', '?')
    videoid = request.args.get("videoid")

    # Eğer videoid None ise, hata döndür
    if not videoid:
        return "Error: 'videoid' parameter is required.", 400

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "tr-TR, tr;q=0.9",
        "origin": "https://www.maltinok.com",
        "referer": "https://www.maltinok.com/",
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    ts = requests.get(source, headers=headers)
    tsal = ts.text

    # Metin işlemleri
    tsal = tsal.replace(f"{videoid}_", f"https://orca-app-y5vl4.ondigitalocean.app/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/{videoid}/1/{videoid}_")
    if "internal" in tsal:
        tsal = tsal.replace('internal', f"https://orca-app-y5vl4.ondigitalocean.app/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/{videoid}/1/internal")
    if "segment" in tsal:
        tsal = tsal.replace('\nmedia', f'\nhttps://orca-app-y5vl4.ondigitalocean.app/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/{videoid}/1/media')

    return tsal

@app.route('/getm3u8', methods=['GET'])
def getm3u8():
    source = request.url.replace('https://orca-app-y5vl4.ondigitalocean.app/getm3u8?source=', '').replace('%2F', '/').replace('%3F', '?')

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "tr-TR, tr;q=0.9",
        "origin": "https://www.maltinok.com",
        "referer": "https://www.maltinok.com/",
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    ts = requests.get(source, headers=headers)
    return ts.text

@app.route('/getstream', methods=['GET'])
def getstream():
    param = request.args.get("param")
    if param == "getts":
        source = request.url.replace('https://orca-app-y5vl4.ondigitalocean.app/getstream?param=getts&source=', '').replace('%2F', '/').replace('%3F', '?')

        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'tr-TR,tr;q=0.9',
            'origin': 'https://www.maltinok.com',
            'referer': 'https://www.maltinok.com/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }

        ts = requests.get(source, headers=headers)
        return ts.content
    elif param == "getm3u8":
        videoid = request.args.get("videoid")
        if not videoid:
            return "Error: 'videoid' parameter is required.", 400

        veriler = {
            "AppId": "3",
            "AppVer": "1025",
            "VpcVer": "1.0.11",
            "Language": "tr",
            "Token": "",
            "VideoId": videoid
        }

        r = requests.post("https://1xlite-900665.top/cinema", json=veriler)
        if "FullscreenAllowed" in r.text:
            veri = r.text
            urls = re.findall(r'"URL":"(.*?)"', veri)
            if urls:
                veri = urls[0].replace("\\/", "__")
                veri = veri.replace('edge3', 'edge10').replace('edge4', 'edge10').replace(':43434', '')

                if "m3u8" in veri:
                    return f"https://orca-app-y5vl4.ondigitalocean.app/{veri}&videoid={videoid}"
        return "Veri yok"

if __name__ == '__main__':
    app.run(debug=True)
