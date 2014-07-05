IP-Updater-For-Heroku
=====================

Enable Naked Domain in Heroku. (For Dozens(http://dozens.jp/) user)


[Dozens](http://dozens.jp/)のAPIを利用して、Herokuでネイキッドドメインを利用できるようにします。  
利用にはDozenzのアカウントとAPIKEYが必要です。  

##利用方法##
dozens_ip_updater/config.pyを編集し、Herokuにデプロイすることで利用することができます。  
1. `git clone https://github.com/LS1qJ/IP-Updater-For-Heroku.git`クローンする  
2. config.pyを編集する(詳細は後述)しする  
3. config.pyの変更をcommitする
    `git add dozens_ip_updater/config.py`
    `git commit -m "setup config.py"`
4. `heroku create fooname` Heroku上にアプリを作成(fooname部分は任意のアプリ名)  
5. `heroku config:add TZ=Asia/Tokyo --app fooname` Herokuのタイムゾーンを設定  
6. `heroku addons:add memcachier:dev --app fooname` HerokuにMemcachierのAddon(無料)を追加  
7. `heroku addons:add papertrail --app fooname` HerokuにLog用のAddon(無料)追加  
8. `git push heroku master` Herokuにアプリをデプロイ  
9. `heroku ps:scale clock=1 --app fooname` Heroku上のアプリを開始  

---
##仕組み##
DozensのAPIを利用してAレコード自動的に更新します。  
下記のルーティンを20分に一度自動実行します。  
* xxx.herokuapp.com　へアクセスし、現在のIPアドレスを取得  
* DozenzAPIを利用して、現在のIPアドレスを独自ドメインのAレコードに設定  

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
