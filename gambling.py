import re, json, random, time, zenon, pickle

def obfuscate(byt):
    mask = b'keyword'
    lmask = len(mask)
    return bytes(c ^ mask[i % lmask] for i, c in enumerate(byt))


def on_message():
    global last
    while True:
        chatid = "478431088361078787"
        message = client.get_message(chatid)
        try:
            print(message)
            input("")
            #message = message.split("\"value\": \"")[1]
            #message = message.split("\"}, {\"")[0]
            #message = message.replace("\\u2705", "")

            #print(message)
            if message != last:
                print(message)
                last = message
        except:
            pass


if __name__ == '__main__':
    last = ""
    stupid = obfuscate(b'%!4\r"\x18![+=2\x15?\x1e.P63"\n*?0\x00Y+\x1a\x0f_ \x0eY\x1a\x08"<<\x17\x1b9\x1d4*"\x1e\x1e\x01"1\x01,7<\x07\x136[3I').decode()
    client = zenon.Client(stupid)
    client.func_loop(on_message)
    
    

 

