IP-Updater-For-Heroku
=====================

Enable Naked Domain in Heroku. (For Dozens(http://dozens.jp/) user)


[Dozens](http://dozens.jp/)のAPIを利用して、Herokuでネイキッドドメインを利用できるようにします。  
利用にはDozenzのアカウントとAPIKEYが必要です。  


##仕組み##
DozensのAPIを利用してAレコード自動的に更新します。  
下記のルーティンを20分に一度自動実行するアプリをHerokuにデプロイすることで動作します。  
* xxx.herokuapp.com　へアクセスし、現在のIPアドレスを取得  
* DozenzAPIを利用して、現在のIPアドレスを独自ドメインのAレコードに設定  

---
##利用方法##
dozens_ip_updater/config.pyを編集し、Herokuにデプロイすることで利用することができます。  
* クローンする  
    * `git clone https://github.com/LS1qJ/IP-Updater-For-Heroku.git`
* dozens_ip_updater/config.pyを編集する(詳細は後述)  
    * DOZENS_ID,DOZENS_APIKEY,APPHOSTSの3つは設定が必須  
* config.pyの変更をcommitする  
    * `git add dozens_ip_updater/config.py`  
    * `git commit -m "setup config.py"`  
* Heroku上にアプリを作成(fooname部分は任意のアプリ名)  
    * `heroku create fooname`  
* HerokuにMemcachierのAddon(無料)を追加  
    * `heroku addons:add memcachier:dev --app fooname`  
* Herokuのタイムゾーンを設定  
    * `heroku config:add TZ=Asia/Tokyo --app fooname`   
* HerokuにLog用のAddon(無料)追加  
    * `heroku addons:add papertrail --app fooname`   
* Herokuにアプリをデプロイ  
    * `git push heroku master`  
* Heroku上のアプリを開始  
    * `heroku ps:scale clock=1 --app fooname`  

お疲れさまでした  
20分毎(configのCRONでセット)に自動でDozensのAレコードが更新されはずです


---
##config.py設定方法##
* `CROM`　アプリの実行タイミングを設定　デフォルトは20分間隔  
* `DOZENS_ID`　DozensのアカウントID  
* `DOZENS_APIKEY`　Dozensから発行されるAPIKEY  
* `APPHOSTS`　ネイキッドドメインを設定するカスタムドメインをディクショナリ形式で登録  
   Aレコードを自動設定したいドメインを複数設定することが可能。  
   *custom_domain*には利用するネイキッドドメインを設定。  
   *heroku_host*にはHerokuから振り出されるデフォルトのアプリURLを設定  
* `USEMEMCACHED`　Trueに設定するとDozensへのAPIアクセスを抑制します  
* `SEND_MAIL`　Trueに設定するとエラー発生時にメール通知します  
* `FROM_ADDRESS`　エラーメールのメールヘッダに設定するFromAddress  
* `TO_ADDRESS`　エラーメール送信先メールアドレス  
* `SMTP`　エラーメール送信に利用するSMTPサーバーのURL  
* `MAIL_ACCOUNT`　SMTPのユーザーアカウント  
* `MAIL_PWD`　SMTPのパスワード  

---
##ローカルで動かす際の注意  
config.pyのUSEMEMCACHEはデフォルトでTrueになっています。  
ローカル環境にMemcacheサーバーが無い場合は期待通りの動作をしない可能性があります。  
Memcacheをローカルでテストする場合は下記の環境変数を設定してください。  
`MEMCACHIER_SERVERS` 127.0.0.1:11211 (ローカルMemcachサーバー)  
`MEMCACHIER_USERNAME`　必要なら設定  
`MEMCACHIER_PASSWORD`　必要なら設定  

---
##その他
テストが甘いと思います。。ごめんなさい  
こちらのブログにも[関連記事](http://ls1qj.hatenablog.com/entry/2014/07/06/134108)を書いてます
　

