import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, timedelta, datetime
from discord_webhook import DiscordWebhook, DiscordEmbed

#team urls
ducks_url = 'https://www.cbssports.com/nhl/teams/TOR/toronto-maple-leafs/schedule/'
# url2 = 'https://www.cbssports.com/nhl/teams/OTT/ottawa-senators/schedule/'

#calculates time for all
today = date.today()

#assigns webhooks mapping to different channel webhooks.
webhook_urls = {
    # 'CFA': 'https://discord.com/api/webhooks/1021281696752082965/83uumkKzGhG_60jfjn97GPmtXDp533-kJZlgt66qhL46Tm-XGoFWMAjs4a0IuGNJSfbc',
    'Chipotle': 'https://discord.com/api/webhooks/1022345453087494245/iZxFDn0sWKljOzMT-253TW2h3_v3jVmbpH5VcyfRtBSqZhMhFL-Qn99GH7QNkScKwGSD'
}

webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1022345453087494245/iZxFDn0sWKljOzMT-253TW2h3_v3jVmbpH5VcyfRtBSqZhMhFL-Qn99GH7QNkScKwGSD', username="CA Chefs")

# webhook = DiscordWebhook(url=webhook_urls.values(), username="CA Chefs")

#receives all stats from web page
def get_stats(url):
    global game_date
    global convert_date
    global home_game
    global results
    global score
    global home_win_score
    global home_loss_score
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table', class_='TableBase-table')
    for team in table.find_all('tbody'):
        rows = team.find_all('tr')
        for row in rows:
            try:
                game_date = row.find('td', class_='TableBase-bodyTd').text.strip()
                convert_date = datetime.strptime(game_date, '%b %d, %Y').date()
                if convert_date == today:
                    home_game = row.find('span', class_='CellLogoNameLockup-opposingPrefix').text.strip()
                    results = row.find('div', class_='CellGame').text.split(' ')[0]
                    score = row.find('div', class_='CellGame').text.split(' ')[1].split('-')
                    link = row.find('div', class_='CellGame', href=True)
                    print(link['href'])
                    if results == 'W':
                        home_win_score = int(score[0])
                        # away_loss_score = int(score[1])
                        # print(home_win_score)
                    else:
                        home_loss_score = int(score[1])
                        # away_win_score = int(score[0])
                        # print(home_loss_score)
                    # print(game_date, convert_date, home_game, results, score)
            except:
                pass

#Runs all team specific promos

def ducks_cfa(url):
    cfa = 'Ducks scored more than 5 runs! Check your app to redeem a free sandwich before 10:30AM PST the following day!'

    # Chick-fil-A's requirement: Ducks score more than 5 runs at home.
    runs = 2
    if home_game != '@':
        if results == 'W':
            try:
                if home_win_score >= runs:
                    try:
                        # Discord Logic
                        embed = DiscordEmbed(title='Chick-Fil-A Sandwich Alert', description=cfa, color='FF0000')
                        embed.add_embed_field(name='Date', value=game_date, inline=True)
                        embed.add_embed_field(name='Region', value='Southern California', inline=True)
                        embed.set_image(url='https://cms.nhl.bamgrid.com/images/photos/326570796/1536x864/cut.png')
                        # embed.set_image(url='https://i.pinimg.com/originals/c9/e6/2f/c9e62f19246adcaf9b64897be3d3bda0.gif')
                        embed.set_footer(text='Powered by CA Chef Foodies', icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                        embed.set_timestamp()
                        webhook.add_embed(embed)

                        # print('winner')
                    except:
                        pass
            except:
                pass
        else:
            try:
                if home_loss_score >= runs:
                    try:
                        # Discord Logic
                        embed = DiscordEmbed(title='Chick-Fil-A Sandwich Alert', description=cfa, color='FF0000')
                        embed.add_embed_field(name='Date', value=game_date, inline=True)
                        embed.add_embed_field(name='Region', value='Southern California', inline=True)
                        embed.set_image(url='https://cms.nhl.bamgrid.com/images/photos/326570796/1536x864/cut.png')
                        # embed.set_image(url='https://i.pinimg.com/originals/c9/e6/2f/c9e62f19246adcaf9b64897be3d3bda0.gif')
                        embed.set_footer(text='Powered by CA Chef Foodies', icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                        embed.set_timestamp()
                        webhook.add_embed(embed)
                        # print('loser')
                    except:
                        pass
            except:
                pass

def ducks_mcd(url):
    mcd = 'Ducks Win! Whenever the Ducks win a home game, fans can score a Big Mac for $2 the following day at any participating McDonalds!'

    # McDonalds requirement: Ducks win at home.
    if home_game != '@':
        if results == 'W':
            # Discord Logic
            embed = DiscordEmbed(title='McDonalds Alert', description=mcd, color='FF0000')
            embed.add_embed_field(name='Date', value=game_date, inline=True)
            embed.add_embed_field(name='Region', value='Southern California', inline=True)
            embed.set_image(url='https://cms.nhl.bamgrid.com/images/photos/326793996/960x540/cut.png')
            # embed.set_image(url='https://i.pinimg.com/originals/c9/e6/2f/c9e62f19246adcaf9b64897be3d3bda0.gif')
            embed.set_footer(text='Powered by CA Chef Foodies', icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
            embed.set_timestamp()
            webhook.add_embed(embed)


def ducks(url):
    today_stats = get_stats(url)
    ducks_cfa(url)
    ducks_mcd(url)

# ducks(ducks_url)
get_stats(ducks_url)

# response = webhook.execute()
