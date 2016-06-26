# FaceCutting

## 説明
Google Cloud Vision APIを利用して顔画像を切り出します。  
Cloud Vision APIの推奨サイズにリサイズした画像を送信します。  
その結果を元に、元画像から顔画像を切り出します。  
指定したフォルダ内のjpgを対象にします。  
指定したフォルダ内にfacesフォルダを作成し、その中に顔画像を出力します。  
出力する画像名は、
[元画像名]\_face[顔数].[元拡張子]  
例）IMG\_1000.JPG → IMG\_1000\_face0.JPG


## 使い方
1. 自分のAPIキーを入力  
1. python face_cutting.py 画像フォルダ
1. 画像フォルダ内のfacesフォルダを確認する