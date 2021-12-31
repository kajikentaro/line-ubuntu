from fastapi import FastAPI, Request, BackgroundTasks  # 🌟BackgroundTasksを追加
from linebot import WebhookParser
from linebot.models import TextMessage
from aiolinebot import AioLineBotApi

# APIクライアントとパーサーをインスタンス化
line_api = AioLineBotApi(
    channel_access_token="RDpXRWqcZUa5ijiI0uc3OsevO6hMZ31YWf6rrbn5IqxPewu5OnSzOPAkPoiV1mw21PmYh8nYerLlRUwU0ikdvFMWy7Zw8Gfpx3xEwBYW5aBAE9/L1B5hJyoKjW8gEC4TAFLN4AI0JjLAkashl/KYDgdB04t89/1O/w1cDnyilFU=")
parser = WebhookParser(channel_secret="2bf8f65f2d64f35dda75ec5dedd57dd2")

# FastAPIの起動
app = FastAPI()

# 🌟イベント処理（新規追加）


async def handle_events(events):
    for ev in events:
        try:
            await line_api.reply_message_async(
                ev.reply_token,
                TextMessage(text=f"You said: {ev.message.text}"))
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
