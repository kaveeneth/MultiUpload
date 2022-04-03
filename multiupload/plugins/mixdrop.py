'''MultiUpload, An Telegram Bot Project
Copyright (c) 2021 Anjana Madu and Amarnath CDJ <https://github.com/AnjanaMadu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>'''

import asyncio, os, requests, time
from requests import post
from multiupload import anjana
from telethon.sync import events, Button
from multiupload.fsub import *
from multiupload.utils import downloader, humanbytes
from config import LOG_CHANNEL

@anjana.on(events.NewMessage(pattern='^/mixdrop'))
async def mixdrop(event):
	user_id = event.sender_id
	if event.is_private and not await check_participant(user_id, f'@{os.environ.get("CHNLUSRNME")}', event):
		return
	if event.reply_to_msg_id:
		pass
	else:
		return await event.edit("Please Reply to File")

	async with anjana.action(event.chat_id, 'typing'):
		await asyncio.sleep(2)
	msg = await event.reply("**Processing...**")
	amjana = await event.get_reply_message()


	## LOGGING TO A CHANNEL
	xx = await event.get_chat()
	reqmsg = f'''Req User: [{xx.first_name}](tg://user?id={xx.id})
FileName: {amjana.file.name}
FileSize: {humanbytes(amjana.file.size)}
#MIXDROP'''
	await anjana.send_message(LOG_CHANNEL, reqmsg)

	result = await downloader(
		f"downloads/{amjana.file.name}",
		amjana.media.document,
		msg,
		time.time(),
		f"**🏷 Downloading...**\n➲ **File Name:** {amjana.file.name}",
	)

	async with anjana.action(event.chat_id, 'document'):
		await msg.edit("Now Uploading to MixDrop")
		data = {
			'email': 'plasmodi@makesnte.com',
			'key': 'crLFRApkOWtQvDzrWwtJ',
		}
		url = "https://ul.mixdrop.co/api"
		r = post(url, stream=True, files={'file': open(f'{result.name}','rb')}, data=data)
	await anjana.action(event.chat_id, 'cancel')

	hmm = f'''File Uploaded successfully !!
Server: MixDrop

**~ File name:** __{amjana.file.name}__
**~ File size:** __{humanbytes(amjana.file.size)}__
NOTE: Files will be deleted after 60 days of inactivity.'''
	await msg.edit(hmm, buttons=(
		[Button.url('📦 Download', "https://mixdrop.co/f/"+r.json()['result']['fileref'])],
		[Button.url('Support Chat 💭', 't.me/KN_URL_Support')]
		))

	os.remove(result.name)
