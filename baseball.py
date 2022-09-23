import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, timedelta, datetime
from discord_webhook import DiscordWebhook, DiscordEmbed

#team urls
angels_url = 'https://www.cbssports.com/mlb/teams/LAA/los-angeles-angels/schedule/'
cubs_url = 'https://www.cbssports.com/mlb/teams/CHC/chicago-cubs/schedule/'
dodgers_url = 'https://www.cbssports.com/mlb/teams/LAD/los-angeles-dodgers/schedule/'
rockies_url = 'https://www.cbssports.com/mlb/teams/COL/colorado-rockies/schedule/'

#calculates time for all
today = date.today()

#assigns webhooks mapping to different channel webhooks.
webhook_urls = {
    # 'CFA': 'https://discord.com/api/webhooks/1021281696752082965/83uumkKzGhG_60jfjn97GPmtXDp533-kJZlgt66qhL46Tm-XGoFWMAjs4a0IuGNJSfbc',
    'Chipotle': 'https://discord.com/api/webhooks/1022345453087494245/iZxFDn0sWKljOzMT-253TW2h3_v3jVmbpH5VcyfRtBSqZhMhFL-Qn99GH7QNkScKwGSD'
}

webhook = DiscordWebhook(url=webhook_urls.values(), username="CA Chefs")

#receives all stats from web page
def get_stats(url):
    global game_date
    global convert_date
    global home_game
    global results
    global score
    global win_score
    global loss_score
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
                    if results == 'W':
                        win_score = int(score[0])
                        # print(win_score)
                    else:
                        loss_score = int(score[1])
                        # print(loss_score)
                    # print(game_date, convert_date, home_game, results, score)
            except:
                pass

#Runs all team specific promos
def angels_mcd(result):
    mc_win = "Angel's Win! \n\nWhenever the Angels win at home, fans get the World Famous medium fries for FREE the following day with a ONE dollar minimum purchase from the McDonalds App. Download and register on the McDonald's App to receive this offer. Only valid within the Greater LA/Orange County DMA."

    if home_game != '@':
        if results == 'W':
                embed = DiscordEmbed(title='McDonalds Win Alert', description=mc_win, color='FF0000')
                embed.add_embed_field(name='Date', value=game_date, inline=True)
                embed.add_embed_field(name='Region', value='Southern California', inline=True)
                embed.set_image(url='https://i.pinimg.com/originals/c9/e6/2f/c9e62f19246adcaf9b64897be3d3bda0.gif')
                embed.set_footer(text='Powered by CA Chef Foodies', icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                embed.set_timestamp()
                webhook.add_embed(embed)
            # print('hello')

def angels_cfa(team_score):

    no_cfa = "Angels didn't score more than 7 runs. No free sandwiches!"
    cfa = 'Angels scored more than 7 runs! Check your app to redeem a free sandwich before 10:30AM PST the following day!'

    # Chick-fil-A's requirement: Angels score more than 7 runs at home.
    runs = 7
    if home_game != '@':
        try:
            if win_score >= runs:
                try:
                    # Discord Logic
                    embed = DiscordEmbed(title='Chick-Fil-A Sandwich Alert', description=cfa, color='FF0000')
                    embed.add_embed_field(name='Date', value=game_date, inline=True)
                    embed.add_embed_field(name='Region', value='Southern California', inline=True)
                    embed.set_image(url='https://media.discordapp.net/attachments/932518403032363058/1020721271379607694/IMG_1501.png?width=312&height=675')
                    # embed.set_image(url='https://i.pinimg.com/originals/c9/e6/2f/c9e62f19246adcaf9b64897be3d3bda0.gif')
                    embed.set_footer(text='Powered by CA Chef Foodies', icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                    embed.set_timestamp()
                    webhook.add_embed(embed)
                except:
                    pass
        except:
            if loss_score >= runs:
                try:
                    # Discord Logic
                    embed = DiscordEmbed(title='Chick-Fil-A Sandwich Alert', description=cfa, color='FF0000')
                    embed.add_embed_field(name='Date', value=game_date, inline=True)
                    embed.add_embed_field(name='Region', value='Southern California', inline=True)
                    embed.set_image(url='https://media.discordapp.net/attachments/932518403032363058/1020721271379607694/IMG_1501.png?width=312&height=675')
                    # embed.set_image(url='https://i.pinimg.com/originals/c9/e6/2f/c9e62f19246adcaf9b64897be3d3bda0.gif')
                    embed.set_footer(text='Powered by CA Chef Foodies', icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                    embed.set_timestamp()
                    webhook.add_embed(embed)
                except:
                    pass

def cubs_cfa(url):
    #Cubs Requirements: Win at home.
    no_cfa = "Chicago Cubs didn't win at home, no free sandwiches!"
    cfa = 'Chicago Cubs win! Check your app to redeem a free sandwich before 10:30AM CDT the following day!'

    if home_game != '@':
        if results == 'W':
            embed = DiscordEmbed(title='Chick-Fil-A Sandwich Alert', description=cfa, color='FF0000')
            embed.add_embed_field(name='Date', value=game_date, inline=True)
            embed.add_embed_field(name='Region', value='Chicago', inline=True)
            embed.set_image(url='https://content.sportslogos.net/logos/54/54/full/wfumtjgnhk5dw395hpkfcwp7e.gif')
            embed.set_footer(text='Powered by CA Chef Foodies',icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
            embed.set_timestamp()
            webhook.add_embed(embed)

def dodgers_cpk(url):
    #Dodgers Requirements. Win at home.
    no_cpk = "Dodger's Lose! No free pizza from California Pizza Kitchen."
    cpk = "Dodger's Win! Check your California Pizza Kitchen rewards section to claim free 7 inch Pizza for Socal regions!"

    if results == 'W':
        # Discord Logic
        embed = DiscordEmbed(title='California Pizza Kitchen Alert', description=cpk, color='FF0000')
        embed.set_author(name='Foodie Bot',icon_url='https://images.getbento.com/accounts/8f224f281c0b0dc913515231c0f0fb7b/media/images/38208little_chef_logo_01.png')
        embed.add_embed_field(name='Date', value=game_date, inline=True)
        embed.add_embed_field(name='Region', value='Southern California', inline=True)
        embed.set_image(url='https://cdn.sanity.io/images/91ree6di/production/2e9b3c2e24e53d8fe4a59b30a972b05bbca1cee7-1140x400.png')
        embed.set_footer(text='Powered by CA Chef Foodies',icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
        embed.set_timestamp()
        webhook.add_embed(embed)
        embed.add_embed_field(name='More Info', value='https://www.cpk.com/dodgers', inline=False)

def dodgers_mcd(url):
    #Dodgers Requirements. Win at home and score more than 6 runs.
    mcd = 'Free 6 piece McNuggets with a purchase of any small fry.'
    runs = 6

    if home_game != '@':
        try:
            if win_score >= runs:
                try:
                    # Discord Logic
                    embed = DiscordEmbed(title='McDonalds Alert', description=mcd, color='FF0000')
                    embed.add_embed_field(name='Date', value=game_date, inline=True)
                    embed.add_embed_field(name='Region', value='Southern California', inline=True)
                    embed.set_image(url='https://pbs.twimg.com/media/D71PauAXUAE5mYP?format=jpg&name=large')
                    embed.set_footer(text='CA Chef Foodies',icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                    embed.set_timestamp()
                    webhook.add_embed(embed)
                except:
                    pass
        except:
            if loss_score >= runs:
                try:
                    # Discord Logic
                    embed = DiscordEmbed(title='McDonalds Alert', description=mcd, color='FF0000')
                    embed.add_embed_field(name='Date', value=game_date, inline=True)
                    embed.add_embed_field(name='Region', value='Southern California', inline=True)
                    embed.set_image(url='https://pbs.twimg.com/media/D71PauAXUAE5mYP?format=jpg&name=large')
                    embed.set_footer(text='CA Chef Foodies',icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                    embed.set_timestamp()
                    webhook.add_embed(embed)
                except:
                    pass

def rockies_tb(url):
    #Rockies Requirements. Win at home and score more than 7 runs.
    tb = 'Rockies scored more than 7 runs! \n\nFrom 4PM to 6PM local time, Taco Bell are offering four (4) regular crunchy tacos for $2. You must order four tacos to redeem the offer. \n\nThe offer is only valid in-restaurant at participating locations within the Denver metro area, not online or via any third-party delivery service. (The offer excludes any other tacos on the menu — only regular crunchy tacos.)'
    runs = 7

    if results == 'W':
        try:
            if win_score >= runs:
                try:
                    # Discord Logic
                    embed = DiscordEmbed(title='Taco Bell Alert', description=tb, color='FF0000')
                    embed.add_embed_field(name='Date', value=game_date, inline=True)
                    embed.add_embed_field(name='Region', value='Denvor Metro Area', inline=True)
                    embed.set_image(url='https://pbs.twimg.com/media/CmnPWAsUMAA2d68.jpg')
                    embed.set_footer(text='CA Chef Foodies',icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                    embed.set_timestamp()
                    webhook.add_embed(embed)
                except:
                    pass
        except:
                try:
                    if loss_score >= runs:
                        # Discord Logic
                        embed = DiscordEmbed(title='Taco Bell Alert', description=tb, color='FF0000')
                        embed.add_embed_field(name='Date', value=game_date, inline=True)
                        embed.add_embed_field(name='Region', value='Denvor Metro Area', inline=True)
                        embed.set_image(url='https://pbs.twimg.com/media/CmnPWAsUMAA2d68.jpg')
                        embed.set_footer(text='CA Chef Foodies',icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                        embed.set_timestamp()
                        webhook.add_embed(embed)
                except:
                    pass

#runs all teams
def rockies(url):
    todays_stats = get_stats(url)
    rockies_tb(url)

def dodgers(url):
    todays_stats = get_stats(url)
    dodgers_cpk(url)
    dodgers_mcd(url)

def cubs(url):
    todays_stats = get_stats(url)
    cubs_cfa(url)

def angels(url):
    todays_stats = get_stats(url)
    angels_mcd(url)
    angels_cfa(url)

angels(angels_url)
cubs(cubs_url)
dodgers(dodgers_url)
rockies(rockies_url)

response = webhook.execute()
