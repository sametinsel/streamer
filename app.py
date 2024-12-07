import requests
from flask import Flask, request
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

@app.route('/<m3u8>')
def index(m3u8):
    try:
        print("Başlangıç: Gelen m3u8 isteği:", request.url)
        m3u8 = request.url.replace('__', '/')
        source = m3u8
        source = source.replace('https://orca-app-y5vl4.ondigitalocean.app/', '')
        source = source.replace('%2F', '/')
        source = source.replace('%3F', '?')
        videoid = request.args.get("videoid")
        print("Video ID:", videoid)

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "tr-TR, tr;q=0.9",
            "origin": "https://www.maltinok.com",
            "referer": "https://www.maltinok.com/",
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }

        ts = requests.get(source, headers=headers)
        print("Kaynak isteği başarılı, durum kodu:", ts.status_code)

        tsal = ts.text
        print("Orijinal kaynak:", tsal[:200])  # İlk 200 karakteri yazdır
        tsal = tsal.replace(videoid+'_', f'https://orca-app-y5vl4.ondigitalocean.app/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/{videoid}/1/{videoid}_')
        if "internal" in tsal:
            tsal = tsal.replace('internal', f'https://orca-app-y5vl4.ondigitalocean.app/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/{videoid}/1/internal')
        if "segment" in tsal:
            tsal = tsal.replace('\n'+'media', '\n' + f'https://orca-app-y5vl4.ondigitalocean.app/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/{videoid}/1/media')
        return tsal
    except Exception as e:
        print("Hata index fonksiyonunda:", str(e))
        return f"Hata oluştu: {str(e)}", 500

@app.route('/getm3u8', methods=['GET'])
def getm3u8():
    try:
        print("Başlangıç: getm3u8 isteği:", request.url)
        source = request.url.replace('https://orca-app-y5vl4.ondigitalocean.app/getm3u8?source=', '')
        source = source.replace('%2F', '/')
        source = source.replace('%3F', '?')

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "tr-TR, tr;q=0.9",
            "origin": "https://www.maltinok.com",
            "referer": "https://www.maltinok.com/",
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }

        ts = requests.get(source, headers=headers)
        print("Kaynak isteği başarılı, durum kodu:", ts.status_code)

        tsal = ts.text
        print("Orijinal kaynak:", tsal[:200])  # İlk 200 karakteri yazdır
        tsal = tsal.replace(videoid+'_', f'https://orca-app-y5vl4.ondigitalocean.app/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/{videoid}/1/{videoid}_')
        return tsal
    except Exception as e:
        print("Hata getm3u8 fonksiyonunda:", str(e))
        return f"Hata oluştu: {str(e)}", 500

@app.route('/getstream', methods=['GET'])
def getstream():
    try:
        param = request.args.get("param")
        print("getstream isteği, param:", param)

        if param == "getts":
            source = request.url.replace('https://orca-app-y5vl4.ondigitalocean.app/getstream?param=getts&source=', '')
            source = source.replace('%2F', '/')
            source = source.replace('%3F', '?')

            headers = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'tr-TR,tr;q=0.9',
                'origin': 'https://www.maltinok.com',
                'referer': 'https://www.maltinok.com/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
            }

            ts = requests.get(source, headers=headers)
            print("Kaynak isteği başarılı, durum kodu:", ts.status_code)
            return ts.content

        elif param == "getm3u8":
            videoid = request.args.get("videoid")
            print("getm3u8 isteği için videoid:", videoid)

            veriler = {
                "AppId": "3", "AppVer": "1025", "VpcVer": "1.0.11",
                "Language": "tr", "Token": "", "VideoId": videoid
            }
           r = requests.post("https://1xlite-900665.top/cinema", json=veriler, timeout=30)
            print("Post isteği tamamlandı, durum kodu:", r.status_code)
            print("Yanıt:", r.text[:500])  # İlk 500 karakteri yazdır

            if "FullscreenAllowed" in r.text:
                veri = re.findall('"URL":"(.*?)"', r.text)
                if not veri:
                    print("Regex ile URL bulunamadı.")
                    return "Veri yok"

                veri = veri[0].replace("\\/", "__")
                veri = veri.replace('edge100', 'edge10')
                print("İşlenmiş URL:", veri)

                if "m3u8" in veri:
                    return f"https://orca-app-y5vl4.ondigitalocean.app/{veri}&videoid={videoid}"
            else:
                print("Yanıtta 'FullscreenAllowed' bulunamadı.")
                return "Veri yok"
    except Exception as e:
        print("Hata getstream fonksiyonunda:", str(e))
        return f"Hata oluştu: {str(e)}", 500

if __name__ == '__main__':
    app.run()
