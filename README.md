# python-slack-bot-2020
pythonにて実装するslack botです。メッセージを送ると反応します。
ZoomAPIを利用してURLを生成します。

## 概要


- SlackアプリをSlackに設定する方法
- GitHub Actionsの基本的な扱い
- Herokuへのデプロイ
- SlackbotからWeb APIを操作して結果をbotが答える
- Zoom APIの利用

Pythonの実行環境は3.7以降を対象にしています。

## ハンズオンに必要な環境

### 対象OS

- Windows 10
- Mac
- Linux

### PCにインストールするもの

- Python 3.7: 公式版をおすすめします。
- エディター,IDE:基本的にお好きな物で
  - Visual Studio Code: 講師が利用します
  - Visual Studio: Python拡張をおすすめします -> [Visual Studio を使用した Python 開発 - Visual Studio | Microsoft Docs](https://docs.microsoft.com/ja-jp/visualstudio/python/?view=vs-2019&fbclid=IwAR0U_6oJEYM8mJB-LcE7XAP6DNobZzlXpvPLNXoev2XiwJQi9gwy0JL0X_w)
  - etc...
- ターミナル
  - Win:コマンドプロンプト（cmd.exe）
  - Mac:ターミナル(iTerm2など)
  - エディター, IDE内蔵のターミナルでも作業できます
- Git: なるべく最新
- Heroku Cli
  - [The Heroku CLI | Heroku Dev Center](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)

### 事前準備

利用する各サービスの登録、 ログインをします

- GitHub
  - [登録](https://github.com/join)
  - [ログイン](https://github.com/login)
- Heroku
  - [登録](https://signup.heroku.com/jp)
  - [ログイン](https://id.heroku.com/login)
- Slack
  - [新規ワークスペース作成](https://slack.com/get-started#/create)

Slackbotを作る際には、開発用のSlackワークスペースを各自で用意することをおすすめします。（Slack側でもアナウンスされています）

サービスの登録については各サービスの案内にしたがってください。

### 作業ディレクトリ

基本的にお好きな場所で構いません。わかりやすい位置としてホームフォルダのドキュメントを基準に操作します。

```cmd
cd ~\Documents
```

### リポジトリをフォークしてClone

GitHubリポジトリを、参加者のGitHubのアカウントへフォークします。そのフォークしたリポジトリをローカル環境にCloneします。

GitHubのフォーク方法はヘルプを確認します。

[リポジトリをフォークする - GitHub ヘルプ](https://help.github.com/ja/github/getting-started-with-github/fork-a-repo)

フォーク後はローカル環境にcloneします。コマンドでの操作はこちらです。
github登録名は適宜書き換えてください。

```cmd
git clone https://github.com/{github登録名}/python-slack-bot-2020.git
```

### ローカル開発環境の用意

Pythonはシステムにインストールされた実行環境以外の仮想環境を用意できます。仮想環境を作ることでシステム側の環境を汚すこと無く開発環境の構築ができます。

仮想環境は以下のコマンドで作成します

```cmd
python -m venv .venv
```

仮想環境を利用するときには、以下のコマンドを実行します。
windowsの場合はこちら

```cmd
.\.venv\Script\activate.bat
```
macの場合はこちら
```cmd
.\.venv\bin\activate
```
仮想環境上に必要なパッケージをインストールします
```cmd
(.venv) > pip install -r requirements.txt
```

仮想環境を終了する場合は以下のコマンドを実行します。

```cmd
(.venv)deactivate
```
## Slackアプリの作成と設定

まず初めにBotとなるSlackアプリをSlack上で作成します。

「Create a Slack App」からApp Nameにアプリ名を入力します。（このアプリ名はHerokuのアプリ名でも利用します。

<img src="https://user-images.githubusercontent.com/55194591/87147422-99b17800-c2e7-11ea-960c-8ff44e173555.png" width=50%>

<b>Slack WorkSpaceはハンズオン用に新たに取得したワークスペースを利用してください。</b>

<img src="https://user-images.githubusercontent.com/55194591/87147427-9ddd9580-c2e7-11ea-9f35-a6aeea34f5cd.png" width=50%>

アプリが作成できたら、「OAuth & Permissions」の「Scopes」>「Bot Token Scopes」にスコープの設定を行います。

<img src="https://user-images.githubusercontent.com/55194591/87147430-9f0ec280-c2e7-11ea-85ee-448121b482fd.png" width=50%>

「Bot Token Scope」はBotとなるSlackアプリがSlackワークスペースに利用できる権限の範囲（スコープ）です。

この時点では`chat:write`のみで、botがSlackへメッセージを送るためのスコープのみを設定していますが、後ほどの設定で、いくつか追加されます。

<img src="https://user-images.githubusercontent.com/55194591/87147435-a0d88600-c2e7-11ea-9004-3f2bf8b87310.png" width=50%>

<br>
<img src="https://user-images.githubusercontent.com/55194591/87147456-a3d37680-c2e7-11ea-9ffa-7d9dfbd1dd30.png" width=50%>

追加したら、ページの上にある「Install App to Workspace」をクリックし、SlackアプリをSlackワークスペースへ追加します。

<img src="https://user-images.githubusercontent.com/55194591/87147460-a504a380-c2e7-11ea-8e8d-30340a895084.png" width=50%>

<img src="https://user-images.githubusercontent.com/55194591/87147484-aa61ee00-c2e7-11ea-8df1-cc43521cac62.png" width=50%>


追加が終わると、「Bot User OAuth Access Token」が表示されます。このトークンをまず控えてください。

<img src="https://user-images.githubusercontent.com/55194591/87147481-a9c95780-c2e7-11ea-83fa-cd84976aba80.png" width=50%>

次に、右上の「Basic Information」へ戻り、「App Credentials」の中にある「Signing Secret」を控えます。

<img src="https://user-images.githubusercontent.com/55194591/87147438-a1711c80-c2e7-11ea-95cd-ad4515060756.png" width=50%>

「Signing Secret」は一度「show」をしてからでないとcopyできないので注意

<img src="https://user-images.githubusercontent.com/55194591/87147445-a2a24980-c2e7-11ea-8406-a5f2c09d84a6.png" width=50%>

### Zoomの登録とAPIの利用

[ZoomAPI](https://marketplace.zoom.us/docs/api-reference/zoom-api)にsign in または Sign upを行う。
その後ドロップダウンメニュー「Develop」から「Build up」を選択する。選択したなかで左側にある「JWT」の「create」をクリックする。

<img src="https://user-images.githubusercontent.com/55194591/87147488-aafa8480-c2e7-11ea-82dc-f311be8a75e0.png" width=50%>

Informationタブに移動し、「App Name」「Company Name」「Name」「Email Address」を入力する。

<img src="https://user-images.githubusercontent.com/55194591/87147476-a8982a80-c2e7-11ea-90bf-c7dafae2eb8e.png" width=50%>


Informationの入力を終えると「Apps Credentials」が見えるようになる。

ここでExpiration Timeにて「other」を選択し、日付を入力する。  
この日付がtokenが使用可能な期限となる。  

(例)23:59 08/11/2020  

2020年8月11日の23:59まで使用可能なTOKENとなる。ここで生成されたTOKENをコピーして手元にメモしておく。(後ほど利用します)


### Herokuのアプリを作成する

Herokuのアプリを作成して必要な設定を行います。

まずHerokuのdashboardへアクセスして「New」>「Create New app」を選択します。

App nameへSlackアプリのアプリ名を入れます。このアプリ名はHerokuアプリの外部アドレスに利用されるので、Heroku内でアプリ名が被る場合に利用できないと出ます。

<img src="https://user-images.githubusercontent.com/55194591/87147449-a33ae000-c2e7-11ea-9cfb-fc726634aae9.png" width=50%>

作成されると、Herokuアプリ名のメニューに入ります。

### Herokuの環境変数にSlackbotで利用するシークレットを登録

Slackbotが実際に動作する環境がHerokuになります。そのため、Herokuの実行環境にSlackbotがSlackと通信する際に利用するapiのトークンやシークレットを覚えさせる必要があります。

Herokuのアプリメニューにある「Settings」の「Config Vars」へ以下の5つを登録します。

|KEY|VALUE|
|---|---|
|SLACK_BOT_TOKEN|Slackアプリ設定で控えた「Bot User OAuth Access Token」|
|SLACK_SIGNING_SECRET|Slackアプリ設定で控えた「Signing Secret」|
|ZOOM_TOKEN|zoom apiにて控えた「Zoom Token」|
|ZOOM_USER_ID|zoomに登録した際のメールアドレス|



<img src="https://user-images.githubusercontent.com/55194591/87147458-a46c0d00-c2e7-11ea-8c11-afef1a0d9082.png" width=70%>

<img src="https://user-images.githubusercontent.com/55194591/87147471-a766fd80-c2e7-11ea-90f3-632b5e52a767.png" width=70%>



### Herokuの認証情報を取得する

Heroku Cli（herokuコマンド）で連携時に必要な認証情報を取得します。

ローカル開発環境でherokuのログインを行います。

```cmd
heroku login

heroku: Press any key to open up the browser to login or q to exit:
Opening browser to https://cli-auth.heroku.com/auth/cli/browser/******[専用のトークン文字列が出ます]
Logging in... done
Logged in as ***@**.com
```

ログイン後、HerokuのAPI Keyを表示して控えてください。

```cmd
heroku auth:token

 »   Warning: token will expire **/**/****
 »   Use heroku authorizations:create to generate a long-term token
[api keyが表示されます]
```

注意:このAPI Keyは外部に漏らさないように注意してください。Herokuへの全権限を持った認証キーとなります。


### GitHub ActionsでHerokuへデプロイ

GitHub ActionsはCI/CDと呼ばれている、継続的なアプリのデプロイを行うサービスです。

[Actions | GitHub](https://github.co.jp/features/actions)

GitHubのリポジトリでは基本的に利用できます。定義ファイルとなる `.github/workflows/*.yml`を用意することで、GitHubのリポジトリにPush, PRなどを行うことで自動的にデプロイをします。`*.yml`ファイルはワークフローと呼ばれています。

今回は、GitHubへ変更のpushを行ったときに自動的にHerokuへデプロイを行う設定を用意しています。

[Herokuへのデプロイを行う workflow.yml](.github/workflows/workflow.yml)

このワークフローは変数を設定しています。HerokuのAPI Key、Herokuのアプリ名、Herokuでログインするときのメールアドレスの3つを設定します。

フォークしたハンズオンのプロジェクトページから「Settings」ページへ進み、「Secrets」のページへ進みます。

<img src="https://user-images.githubusercontent.com/55194591/87151453-d7fe6580-c2ee-11ea-937a-f81fbd0c0dde.png" width=70%>

「New secret」ボタンから変数を追加します。

|変数名|値|
|---|---|
|HEROKU_API_KEY|[`heroku auth:token` で取得したトークン]|
|HEROKU_APP_NAME|[Herokuのアプリ名]|
|HEROKU_EMAIL|[Herokuのログインで利用するメールアドレス]|

<br>
<img src="https://user-images.githubusercontent.com/55194591/87151463-db91ec80-c2ee-11ea-9a18-2b76c67390e5.png" width=80%>


Actionsを動作させます。今回のワークフローでは、GitHubへ変更をpushしたタイミングで自動的にワークフローが動作します。なので何かしらのファイルを追加してcommitします。

ローカル開発環境にてREADMEを編集する。

```cmd
git add .
git commit -m "add new file"

git push origin master
```

pushが終わるとGitHub ActionsとHeroku側でそれぞれデプロイ作業が始まります。

終了したときのGitHubとHerokuの結果はこのように表示されます。

### Slackbotが利用できるイベントを登録する

Slack Event APIを使い、Slackワークスペース上に起きたイベントを、Slackbotが動作するサーバー(ここではHeroku)へ伝えることができます。

ここで2つの設定を行います。

1. Slack Event APIが起きたイベントをサーバーに伝えるためのエンドポイントURL
2. イベントの種類

まず1つめの、Slack Event APIが起きたイベントをサーバーに伝えるためのエンドポイントURLを設定します。

「Event Subscriptions」ページの「Enable Events」にある、右上のボタンをOnにします。

次に「Request URL」にエンドポイントURLを設定します。Herokuのアプリ上でbotアプリが待機しているアドレスを入力します。

> https://[Herokuのアプリ名].herokuapp.com/slack/events

<img src="https://user-images.githubusercontent.com/55194591/87151465-dcc31980-c2ee-11ea-9254-44eed805e202.png" width=70%>

2つ目の、イベントの種類を登録します。

イベントには種類があり、あらかじめアプリで取得したいイベントの種類を登録する必要があります。

Slackアプリのスコープを扱ったときに、イベントによるスコープの決定もあると書きましたが、このイベントを登録することでスコープの変化もあります。

「Event Subscriptions」の「Subscribe to bot events」内に`message.channels`イベントを登録します。

<img src="https://user-images.githubusercontent.com/55194591/87151469-dd5bb000-c2ee-11ea-9d28-bc38613b3adf.png" width=70%>


登録後はSlackワークスペースへアプリの再インストールを指示されるので行います。


再インストール時の認証画面を見ると、権限が追加されていることがわかります。先ほどはチャンネルにメッセージを送信するだけでしたが、それに加えてチャンネル内のメッセージを見ることができます。


デプロイとSlackアプリの権限の設定が終わると、Slackbotが利用できます。最後にSlackワークスペース上でbotを呼び出してみます。

最初に、チャンネルにbotユーザーを追加します。


次に、botが反応するワードをポストします。ポストして数秒で返答されるようになっています。

「こんにちは」→「こんにちは」

「create」→Zoomのmeetingが作成される

「list」→ ZoomのListが表示される

「deleate」→Zoomの部屋が消去される


## Slackbot概要

システム全体の様子はこのような形になります。


## 参考資料

- [slackapi/python-slack-events-api: Slack Events API adapter for Python](https://github.com/slackapi/python-slack-events-api)
- [slackapi/python-slackclient: Slack Developer Kit for Python](https://github.com/slackapi/python-slackclient)
- [heroku/python-getting-started: Getting Started with Python on Heroku.](https://github.com/heroku/python-getting-started)
- [【Python＋heroku】Python入れてない状態からherokuで何か表示するまで（前編） - Qiita](https://qiita.com/it_ks/items/afd1bdb792d41d0e1145#%E3%83%87%E3%83%97%E3%83%AD%E3%82%A4)
- [API Events | Slack](https://api.slack.com/events)

## おまけ

### ローカル開発環境からHerokuへデプロイする

GitHub Actionsを使ってのデプロイではなく、ローカル環境からHerokuへデプロイする手段を紹介します。

`heroku login`を行った後に、herokuへのデプロイ用のgitリポジトリの登録、pushを行います。

```cmd

heroku git:remote -a [herokuのアプリ名]
git push heroku master
```


こちらを参考にさせていただきました！
https://github.com/kakuemon/py-suruga-13-slackbot-handson

絵文字の参考サイトです
https://www.webfx.com/tools/emoji-cheat-sheet/
