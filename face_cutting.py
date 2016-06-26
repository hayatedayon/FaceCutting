#!/usr/bin/python
#coding:utf-8
import cv2
import os
import sys
import base64
import json
import requests
import glob

# APIのURL
api_url = 'https://vision.googleapis.com/v1/images:annotate?key='

# APIキー
api_key = '自分のAPIキーを入力'

# 出力ディレクトリの作成
dir = os.path.abspath(sys.argv[1])
if not os.path.exists(dir + '/faces'):
    os.mkdir(dir + '/faces')

for f in glob.glob(sys.argv[1]+'/*.jpg'):
    print f
    # 画像ファイルの読み出し
    src = cv2.imread(f)
## Cloud Vision API送信用画像の作成
    # 画像サイズの読み出し
    height, width = src.shape[:2]
    # 画像の変換サイズを計算
    if (height > width):
        rate = round(float(1200) / height, 2)
    else:
        rate = round(float(1600) / width, 2)
    # 元画像サイズの出力
    #print 'rate      :', rate
    #print 'in height :', height
    #print 'in width  :', width
    # 計算サイズを格納
    height = int(height * rate)
    width = int(width * rate)
    # 変換画像サイズの出力
    #print 'out height:', height
    #print 'out width :', width
    # 変換イメージを格納
    new_size = cv2.resize(src, (width, height))
    # 変換イメージの出力
    cv2.imwrite('tmp.jpg', new_size)
## Cloud Vision APIを使う
    # 変換イメージをbase64にエンコード
    base64_image = base64.b64encode(open('tmp.jpg', 'rb').read())
    
    data = {
        'requests': [{
            'image': {
                'content': base64_image,
            },
            'features': [{
                'type': 'FACE_DETECTION',
                'maxResults': 20,
            }]
            
        }]
    }
    
    # リクエスト送信
    header = {'Content-Type': 'application/json'}
    response = requests.post(api_url + api_key,  json.dumps(data), header)
    
    # 分析結果の取得
    if response.status_code == 200:
        #print response.text
## 顔画像の切り出し
        json_response = json.loads(response.text)
        # 顔認識の結果が含まれていれば切り出す
        if json_response['responses'][0].has_key('faceAnnotations'):
            # 認識できた顔の数だけループ
            for i, face in enumerate(json_response['responses'][0]['faceAnnotations']):
                # 顔画像位置
                vertices = [(v.get('x', 0.0), v.get('y', 0.0)) for v in face['fdBoundingPoly']['vertices']]
                #print vertices
                # 元画像用に位置を変換
                x1 = int(vertices[0][0] / rate)
                x2 = int(vertices[2][0] / rate)
                y1 = int(vertices[0][1] / rate)
                y2 = int(vertices[2][1] / rate)
                width = x2 - x1
                height = y2 - y1
                # 切り出しサイズが正方形になるように調整
                if width >= height:
                    y2 = y1 + width
                else:
                    x2 = x1 + height
                #切り出し範囲を格納
                dst = src[y1:y2, x1:x2]
                # 顔画像の出力パスを作成
                root, ext = os.path.splitext(os.path.basename(f))
                face_image_path = dir + '/faces/' + root + '_face' + str(i) + ext
                print face_image_path
                # 顔画像の出力
                cv2.imwrite(face_image_path , dst)
        else:
            print u'顔が認識されませんでした'
    else:
        print 'Http response error'
        print response.status_code

