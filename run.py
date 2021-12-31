from fastapi import FastAPI, Request, BackgroundTasks  # 🌟BackgroundTasksを追加
from linebot import WebhookParser
from linebot.models import TextMessage
from aiolinebot import AioLineBotApi
import main
import os
from dotenv import load_dotenv
load_dotenv()

# APIクライアントとパーサーをインスタンス化
line_api = AioLineBotApi(
    channel_access_token=os.getenv('channel_access_token'))
parser = WebhookParser(channel_secret=os.getenv('channel_secret'))

# FastAPIの起動
app = FastAPI()

dockerenv = main.DockerEnv()

# 🌟イベント処理（新規追加）


async def handle_events(events):
    for ev in events:
        try:
            await line_api.reply_message_async(
                ev.reply_token,
                TextMessage(text=dockerenv.exec(ev.message.text)))
        except Exception:
            # エラーログ書いたりする
            pass


@app.post("/messaging_api/handle_request")
# 🌟background_tasksを追加
async def handle_request(request: Request, background_tasks: BackgroundTasks):
    # リクエストをパースしてイベントを取得（署名の検証あり）
    events = parser.parse(
        (await request.body()).decode("utf-8"),
        request.headers.get("X-Line-Signature", ""))

    # 🌟イベント処理をバックグラウンドタスクに渡す
    background_tasks.add_task(handle_events, events=events)

    # LINEサーバへHTTP応答を返す
    return "ok"
