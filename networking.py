import asyncio
import json
import re
from discordweb import Webhook
import aiohttp
from colorama import Fore, Style
from lomond import WebSocket
from unidecode import unidecode
import question

async def fetch(url, session, timeout):
    try:
        async with session.get(url, timeout=timeout) as response:
            return await response.text()
    except Exception:
        print("Server timeout/error to %s" % url)
        return ""


async def get_responses(urls, timeout, headers):
    tasks = []
    async with aiohttp.ClientSession(headers=headers) as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session, timeout))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses


async def get_response(url, timeout, headers):
    async with aiohttp.ClientSession(headers=headers, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        return await fetch(url, session, timeout)


async def get_json_response(url, timeout, headers):
    async with aiohttp.ClientSession(headers=headers, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get(url, timeout=timeout) as response:
            return await response.json()


async def websocket_handler(uri, headers):
    websocket = WebSocket(uri)
    for header, value in headers.items():
        websocket.add_header(str.encode(header), str.encode(value))
    
    for msg in websocket.connect(ping_rate=5):
        if msg.name == "text":
            message = msg.text
            message = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", message)

            message_data = json.loads(message)

            if "error" in message_data and message_data["error"] == "Auth not valid":
                raise RuntimeError("Connection settings invalid")
            elif message_data["type"] != "interaction":
                if message_data["type"] == "question":
                    question_str = unidecode(message_data["question"])
                    answers = [unidecode(ans["text"]) for ans in message_data["answers"]]
                    print("\n" * 5)
                    print("Question detected.")
                    print("Question %s out of %s" % (message_data['questionNumber'], message_data['questionCount']))
                    with open("uk.txt", "w") as uk:uk.write("\nQuestion %s out of %s" % (message_data['questionNumber'], message_data['questionCount']))
                    aMsg = Fore.CYAN + question_str + "\n"
                    for a in answers:
                        aMsg = aMsg + "\n" + a
                    aMsg = aMsg + Style.RESET_ALL
                    print()
                    await question.answer_question(question_str, answers)

    print("Socket closed")
    
    
async def websocket_lives_handler(uri, bearers, broadid):
    for bearer in bearers:
        headers = {"Authorization": "Bearer %s" % bearer,"x-hq-client": "Android/1.3.0"}
        websocket = WebSocket(uri)
        for header, value in headers.items():
            websocket.add_header(str.encode(header), str.encode(value))
        first = True
        for msg in websocket.connect(ping_rate=5):
            if msg.name == "text":
                message = msg.text
                message = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", message)
                message_data = json.loads(message)

                if "error" in message_data and message_data["error"] == "Auth not valid":
                    print("Connection settings invalid")

                if first == True:
                    websocket.send_json({"authToken":bearer, "type": "subscribe", "broadcastId": broadid})
                    first = False
                else:websocket.close()
