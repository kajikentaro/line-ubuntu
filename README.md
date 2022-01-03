# LINE Messaging API を Ubuntu ターミナルにする
## Feature

- LINE Bot を用いてチャットを Bash で実行した結果をリプライする
- Docker をサンドボックスとして使用
- Available here: [https://line.me/R/ti/p/%40114gaerp](https://line.me/R/ti/p/%40114gaerp)

## デプロイ方法

1. サーバー等にこのリポジトリを clone する
1. `.env.template`を`.env`にコピーし LINE Developers から取得した「チャネルアクセストークン」、「チャネルシークレット」を記述する。
1. docker をインストールし、`docker-compose up` を実行  
   `http://localhost:8000/messaging_api/handle_request`で FastApi が起動する
1. SSL 化を行い、LINE Developers に Web Hook を設定する。

<img src="https://user-images.githubusercontent.com/58505538/147826267-7779ef38-1a4e-400f-8af3-35d62423d0e4.png" width="50%">
