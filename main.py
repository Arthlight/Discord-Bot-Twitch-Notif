"""Twitch Notification Bot

This simple script allows the user to configure their own custom Bot
for the Discord application with the goal of notifying their members
as soon as Twitch streamers of their choosing go live.

Furthermore, this script makes use and is dependant on a .env file
within the same directory in order to store sensitive data such as
needed Tokens and IDs.

This file contains the following class with these affiliated methods:

    class MyClient               - a collection of methods working together in order
                                   to push predefined messages to connected Discord
                                   servers.

    method on_ready              - calls method twitch_info_requested() as soon as
                                   the bot connected to the Discord servers.

    method twitch_info_requested - interacts with the Twitch API in order to determine
                                   if and when predeclared streamers are going live.
                                   In case the API sends back a positive result (i.e.
                                   the streamer just went live), the name of this
                                   streamer gets passed as an argument to
                                   message_sent().

    method message_sent          - accepts the name of a streamer, calls embeds_created()
                                   with that information to retrieve a customized message
                                   for this particular streamer, and finally pushes the
                                   notification onto the Discord servers for the members
                                   to see.

    method embeds_created        - accepts the name of a streamer and creates a respective
                                   customized message in order to send it back to message_sent()
"""

# Standard libraries
import os
import asyncio
import urllib.request
import urllib.parse
import json

# Third party libraries
import discord

from dotenv import load_dotenv

load_dotenv()

# Discord Authentication
token = os.getenv('DISCORD_TOKEN')

# Twitch Authentication
client_id = os.getenv('TWITCH_CLIENT_ID')


class MyClient(discord.Client):

    async def on_ready(self):
        """prompts the methods of the class to run as soon as the client connected to the Discord servers"""
        await self.twitch_info_requested()

    async def embeds_created(self, streamer):
        """creates custom notification messages for streamers.

        Args:
            streamer: the name of the streamer who went live
        Returns:
            a custom notification message for the specified streamer
        """

        dpsosiris_user = client.get_user(309024230895517698)
        arthlight_user = client.get_user(267558514325454869)

        if streamer == 'arthlight':
            arthlight_embed = discord.Embed(
                title='Twitch Notification!',
                description='Arthlight is now live!',
                colour=discord.Colour.from_rgb(66, 185, 245),
            )
            arthlight_embed.set_footer(
                text='Validated by Bitstorm Corporations',
                icon_url='https://ak7.picdn.net/shutterstock/videos/33150397/thumb/1.jpg',
            )
            arthlight_embed.set_image(
                url='https://i.kym-cdn.com/photos/images/original/001/164/653/8d2.gif',
            )
            arthlight_embed.set_author(
                name='Arthlight',
                icon_url=arthlight_user.avatar_url
            )
            arthlight_embed.set_thumbnail(
                url='https://i.pinimg.com/originals/9e/8d/0d/9e8d0db83e84403c79309507bf7e3628.png',
            )
            arthlight_embed.add_field(
                name='Swing by and join the party:',
                value='[twitch.tv/arthlight](https://twitch.tv/arthlight)',
                inline=False,
            )

            return arthlight_embed

        elif streamer == 'dpsosiris':
            dpsosiris_embed = discord.Embed(
                title='Come on in! But leave your weapons by the door...',
                description='[twitch.tv/dpsOsiris](https://twitch.tv/dpsOsiris)',
                colour=discord.Colour.from_rgb(173, 7, 7),
            )
            dpsosiris_embed.set_footer(
                text='Validated by Bitstorm Corporations',
                icon_url='https://ak7.picdn.net/shutterstock/videos/33150397/thumb/1.jpg'
            )
            dpsosiris_embed.set_image(
                url='https://66.media.tumblr.com/87d0c8ae14b9270700d13dbae8639773/tumblr_phl8xtwtaw1xye92vo1_400.gif'
            )
            dpsosiris_embed.set_author(
                name='dpsosiris',
                icon_url=dpsosiris_user.avatar_url,
            )
            dpsosiris_embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/627097919303974934/634854575815393284/creecree.png',
            )

            return dpsosiris_embed

    async def twitch_info_requested(self):
        """interacts with the Twitch API in order to retrieve the streamers current online statuses"""

        streamer_id = [
            'arthlight',
            'dpsosiris',
        ]
        streamer_count = [
            0,
            0,
        ]

        while True:
            twitch_response = []

            for id in streamer_id:

                twitch_api_url = f'https://api.twitch.tv/helix/streams?user_login='
                client_request_header = {'Client-ID': client_id}
                client_request_stored = urllib.request.Request(twitch_api_url + id, headers=client_request_header)
                client_request_open = urllib.request.urlopen(client_request_stored)
                twitch_response.append(json.loads(client_request_open.read()))

            for index, response in enumerate(twitch_response):
                if response.get('data') and streamer_count[index] < 1:
                    if response.get('data')[0].get('user_name') == 'dpsOsiris':
                        streamer_count[index] += 1
                        await self.message_sent('dpsosiris')
                    elif response.get('data')[0].get('user_name') == 'arthlight':
                        streamer_count[index] += 1
                        await self.message_sent('arthlight')

                elif not response.get('data') and streamer_count[index] > 0:
                    streamer_count[index] = 0

            twitch_response.clear()
            await asyncio.sleep(10)

    async def message_sent(self, streamer):
        """sends a custom notification to a specified Discord channel
        Args:
            streamer: the name of the streamer who went live.
        """

        channel = client.get_channel(635425292252348419)

        if streamer == 'arthlight':
            await channel.send(embed=await self.embeds_created('arthlight'))

        elif streamer == 'dpsosiris':
            await channel.send(embed=await self.embeds_created('dpsosiris'))

        else:
            await channel.send(
              '''
              Something went wrong, check the logs Pegasus! If you see this and he 
              is not currently online, please ping him and you will get a reward!
              '''
             )


client = MyClient()
client.run(token)

























