import asyncio
import websockets
import json
import aiohttp
import base64

GATEWAY_URI = "wss://gateway.discord.gg/?v=10&encoding=json"

def display_ascii_art():
    print("""
    ████████╗ ██████╗ ███╗   ███╗ █████╗ ██╗███╗   ██╗
    ╚══██╔══╝██╔═══██╗████╗ ████║██╔══██╗██║████╗  ██║
       ██║   ██║   ██║██╔████╔██║███████║██║██╔██╗ ██║
       ██║   ██║   ██║██║╚██╔╝██║██╔══██║██║██║╚██╗██║
       ██║   ╚██████╔╝██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
       ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
       ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝""")
    print("Welcome to Tomain")
    print("This tool was developed by Syracuse\n")

def load_tokens(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

async def check_token_validity(tokens):
    valid_tokens = []
    async with aiohttp.ClientSession() as session:
        for token in tokens:
            headers = {"Authorization": token}
            url = "https://discord.com/api/v10/users/@me"
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    print(f"[+] Token valid: {token[:6]}...")
                    valid_tokens.append(token)
                else:
                    print(f"[-] Token invalid: {token[:12]} - Status: {resp.status}")
    return valid_tokens

async def connect_to_gateway(token, guild_id, channel_id, action):
    async with websockets.connect(GATEWAY_URI) as ws:
        identify_payload = {
            "op": 2,
            "d": {
                "token": token,
                "properties": {
                    "$os": "linux",
                    "$browser": "disco",
                    "$device": "disco"
                },
                "presence": {"status": "online", "afk": False}
            }
        }
        await ws.send(json.dumps(identify_payload))
        while True:
            response = json.loads(await ws.recv())
            if response.get("op") == 10 or response.get("t") == "READY":
                break

        voice_state_payload = {
            "op": 4,
            "d": {
                "guild_id": guild_id,
                "channel_id": channel_id if action == "join" else None,
                "self_mute": False,
                "self_deaf": False
            }
        }
        await ws.send(json.dumps(voice_state_payload))
        print(f"[+] Sent {action.upper()} VC request for token {token[:6]}.")

async def spam_messages(token, channel_id, message, repeat_count):
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": token}
        url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        payload = {"content": message}
        for _ in range(repeat_count):
            async with session.post(url, headers=headers, json=payload) as resp:
                if resp.status == 200:
                    print(f"[+] Sent message for token {token[:6]}...")
                else:
                    print(f"[-] Failed to send message for token {token[:6]}: {resp.status}")

async def change_nickname(token, server_id, nickname):
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": token}
        url = f"https://discord.com/api/v10/guilds/{server_id}/members/@me"
        payload = {"nick": nickname}
        async with session.patch(url, headers=headers, json=payload) as resp:
            if resp.status == 200:
                print(f"[+] Nickname changed for token {token[:6]}...")
            else:
                print(f"[-] Failed to change nickname for token {token[:6]}: {resp.status}")

async def update_bio(token, bio):
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": token}
        url = "https://discord.com/api/v10/users/@me"
        payload = {"bio": bio}
        async with session.patch(url, headers=headers, json=payload) as resp:
            if resp.status == 200:
                print(f"[+] Bio updated for token {token[:6]}...")
            else:
                print(f"[-] Failed to update bio for token {token[:6]}: {resp.status}")

async def update_status(token, status, activity_type, activity_name):
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": token}
        activities = [
            {
                "name": activity_name,
                "type": 1 if activity_type.lower() == "streaming" else 0,
                "url": "https://twitch.tv/somechannel" if activity_type.lower() == "streaming" else None
            }
        ]
        payload = {
            "status": status.lower(),
            "activities": activities,
            "afk": False,
            "since": None
        }
        async with session.patch("https://discord.com/api/v10/users/@me/settings", headers=headers, json=payload) as resp:
            if resp.status == 200:
                print(f"[+] Status updated for token {token[:6]}...")
            else:
                print(f"[-] Failed to update status for token {token[:6]}: {resp.status}")

async def main():
    display_ascii_art()
    tokens = load_tokens("tokens.txt")
    if not tokens:
        print("[-] No tokens found in tokens.txt.")
        return

    print("[*] Checking token validity...")
    tokens = await check_token_validity(tokens)
    if not tokens:
        print("[-] No valid tokens available.")
        return

    while True:
        print("""
    ████████╗ ██████╗ ███╗   ███╗ █████╗ ██╗███╗   ██╗
    ╚══██╔══╝██╔═══██╗████╗ ████║██╔══██╗██║████╗  ██║
       ██║   ██║   ██║██╔████╔██║███████║██║██╔██╗ ██║
       ██║   ██║   ██║██║╚██╔╝██║██╔══██║██║██║╚██╗██║
       ██║   ╚██████╔╝██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
       ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
       ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝""")
        print("""
    [1] Spam Messages
    [2] Join Voice Channel
    [3] Leave Voice Channel
    [4] Change Nickname
    [5] Update Bio
    [6] Update Status
    [7] Exit
    """)
        option = input("Option: ")
        if option == "1":
            channel_id = input("Enter the channel ID: ")
            message = input("Enter the message to spam: ")
            repeat_count = int(input("Enter the number of times to spam: "))
            await asyncio.gather(
                *[spam_messages(token, channel_id, message, repeat_count) for token in tokens]
            )
        elif option == "2":
            guild_id = input("Enter the guild ID: ")
            channel_id = input("Enter the voice channel ID: ")
            await asyncio.gather(
                *[connect_to_gateway(token, guild_id, channel_id, "join") for token in tokens]
            )
        elif option == "3":
            guild_id = input("Enter the guild ID: ")
            await asyncio.gather(
                *[connect_to_gateway(token, guild_id, None, "leave") for token in tokens]
            )
        elif option == "4":
            server_id = input("Enter the server ID: ")
            nickname = input("Enter the new nickname: ")
            await asyncio.gather(
                *[change_nickname(token, server_id, nickname) for token in tokens]
            )
        elif option == "5":
            bio = input("Enter the new bio: ")
            await asyncio.gather(
                *[update_bio(token, bio) for token in tokens]
            )
        elif option == "6":
            status = input("Enter the new status (online/dnd/idle/invisible): ")
            activity_type = input("Enter activity type (playing/streaming): ")
            activity_name = input("Enter activity name: ")
            await asyncio.gather(
                *[update_status(token, status, activity_type, activity_name) for token in tokens]
            )
        elif option == "7":
            print("[+] Exiting...")
            break
        else:
            print("[-] Invalid option. Try again.")

if __name__ == "__main__":
    asyncio.run(main())
