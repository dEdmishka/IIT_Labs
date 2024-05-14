from typing import Final
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from http.server import BaseHTTPRequestHandler, HTTPServer
metrics = {
    'some': '10',
    'add': '5',
    'change': '-5',
    'sum': '20',
}

TOKEN: Final = '7034838694:AAH7eQC6ihG_6_FkSUQD-9zI4LSMOhioTIA'
BOT_USERNAME: Final = '@Lab_iit_10_bot'
PORT: Final = 9091


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привіт! Я бот для створення метрик.')


async def create_metric_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.split()
    if len(text) != 3:
        await update.message.reply_text(
            'Неправильний формат команди. Повинно бути: /metrics <назва_метрики> <значення>')
        return
    metric_name = text[1]
    metric_value = text[2]
    print(text)
    metrics[metric_name] = metric_value
    await update.message.reply_text(f'Метрика {metric_name} створена зі значенням {metric_value}')


def main_telegram():
    print('Starting app bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('metrics', create_metric_command))
    print('Polling...')
    app.run_polling(poll_interval=3)


# Web server
class MetricServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        response = "\n".join([f"{metric} {metrics[metric]}" for metric in metrics])
        print(response)
        self.wfile.write(response.encode())


def main_webserver():
    server = HTTPServer(("", PORT), MetricServer)
    print(f"Server running on port {PORT}")
    server.serve_forever()


if __name__ == "__main__":
    _thread = threading.Thread(target=main_webserver)
    _thread.start()
    main_telegram()
