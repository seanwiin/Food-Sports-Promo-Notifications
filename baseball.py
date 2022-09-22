import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, timedelta, datetime
from discord_webhook import DiscordWebhook, DiscordEmbed


# url = 'https://www.baseball-reference.com/teams/LAA/2022-schedule-scores.shtml#team_schedule::1'
angels_url = 'https://www.cbssports.com/mlb/teams/LAA/los-angeles-angels/schedule/'
cubs_url = 'https://www.cbssports.com/mlb/teams/CHC/chicago-cubs/schedule/'
dodgers_url = 'https://www.cbssports.com/mlb/teams/LAD/los-angeles-dodgers/schedule/'
rockies_url = 'https://www.cbssports.com/mlb/teams/COL/colorado-rockies/schedule/'

#calculates time for all
today = date.today()
d = date(2022, 5, 30)
# print(d)
# print(today)

#assigns webhooks mapping to different channel webhooks.

webhook_urls = {
    # 'CFA': 'https://discord.com/api/webhooks/1021281696752082965/83uumkKzGhG_60jfjn97GPmtXDp533-kJZlgt66qhL46Tm-XGoFWMAjs4a0IuGNJSfbc',
    'Chipotle': 'https://discord.com/api/webhooks/1022345453087494245/iZxFDn0sWKljOzMT-253TW2h3_v3jVmbpH5VcyfRtBSqZhMhFL-Qn99GH7QNkScKwGSD'
}
webhook = DiscordWebhook(url=webhook_urls.values(), username="CA Chefs")

# df = pd.DataFrame(columns= ['Gm#', 'Date', 'Box_Score',' Team', 'Home/Away', 'Opp', 'W/L', 'R', 'R/A', 'Inn', 'W-L', 'Rank', 'GB', 'Win' 'Loss', 'Save','Time','D/N','Attendance','cLI','Streak','Orig. Scheduled'])

def baseballreference(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table', attrs={'id': 'team_schedule'})
    date = today - timedelta(days=1)

    for team in table.find_all('tbody'):
        # print(team)
        rows = team.find_all('tr')
        # print(rows)
        for row in rows:
            if row.find('tr', class_='thead'):
                pass
            else:
                pl_date = row.find('td', class_='left', attrs={'data-stat': 'date_game'})
                pl_team = row.find('td', class_='left', attrs={'data-stat': 'opp_ID'})
                pl_home = row.find('td', class_='left', attrs={'data-stat': 'homeORvis'})
                pl_runs = row.find('td', class_='right', attrs={'data-stat': 'R'})
                if pl_date is None:
                    pass
                else:
                    if pl_home.text != '@':
                        try:
                            date_filter1 = pl_date.find('a', href=True)
                            date_filter2 = date_filter1['href'].split('=')[1]
                            convert_date = datetime.strptime(date_filter2, '%Y-%m-%d').date()

                            if convert_date == date:
                                runs = 7
                                angel_runs = int(pl_runs.text)
                                if angel_runs >= runs:
                                    print('Check your CFA')
                                else:
                                    print('No Sandwich')
                        except:
                            pass
# baseballreference(url)

def angels(angels_url):
    page = requests.get(angels_url)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table', class_='TableBase-table')

    no_cfa = "Angels didn't score more than 7 runs. No free sandwiches!"
    cfa = 'Angels scored more than 7 runs! Check your app to redeem a free sandwich before 10:30AM PST the following day!'
    mc_win = "Angel's Win! \n\n Whenever the Angels win at home, fans get the World Famous medium fries for FREE the following day with a ONE dollar minimum purchase from the McDonalds App. Download and register on the McDonald's App to receive this offer. Only valid within the Greater LA/Orange County DMA."

    for team in table.find_all('tbody'):
        rows = team.find_all('tr')
        for row in rows:
            try:
                game_date = row.find('td', class_='TableBase-bodyTd').text.strip()
                convert_date = datetime.strptime(game_date, '%b %d, %Y').date()
                home_game = row.find('span', class_='CellLogoNameLockup-opposingPrefix').text.strip()
                results = row.find('div', class_='CellGame').text.split(' ')[0]
                score = row.find('div', class_='CellGame').text.split(' ')[1].split('-')
                if convert_date == today:
                    if home_game != '@':
                        runs = 7
                        # W = left number and L = right number
                        if results == 'W':
                            # Discord Logic for Mcdonalds
                            embed = DiscordEmbed(title='McDonalds Win Alert', description=mc_win, color='FF0000')
                            # embed.set_thumbnail(url=image_link)
                            embed.add_embed_field(name='Date', value=game_date, inline=True)
                            embed.add_embed_field(name='Region', value='Southern California', inline=True)
                            # embed.add_embed_field(name='Alert Status', value=mc_win, inline=True)
                            embed.set_image(url='https://i.pinimg.com/originals/c9/e6/2f/c9e62f19246adcaf9b64897be3d3bda0.gif')
                            embed.set_footer(text='Powered by CA Chef Foodies',
                                             icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                            embed.set_timestamp()
                            webhook.add_embed(embed)


                            # Discord Logic for CFA
                            loss_score = int(score[1])
                            if loss_score >= runs:
                                # Discord Logic
                                embed = DiscordEmbed(title='Chick-Fil-A Sandwich Alert', description=cfa, color='FF0000')
                                # embed.set_thumbnail(url=image_link)
                                embed.add_embed_field(name='Date', value=game_date, inline=True)
                                embed.add_embed_field(name='Region', value='Southern California', inline=True)
                                # embed.add_embed_field(name='Alert Status', value=cfa, inline=True)
                                embed.set_image(url='https://i.pinimg.com/originals/c9/e6/2f/c9e62f19246adcaf9b64897be3d3bda0.gif')
                                embed.set_footer(text='Powered by CA Chef Foodies',
                                                 icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                                embed.set_timestamp()
                                webhook.add_embed(embed)
                                # response = webhook.execute()
                                # print(convert_date, 'CFA Sandwich Alert')
                            else:
                                # # Discord Logic
                                # embed = DiscordEmbed(title='Chick-Fil-A Sandwich Alert', color='FF0000')
                                # # embed.set_thumbnail(url=image_link)
                                # embed.add_embed_field(name='Date', value=game_date, inline=True)
                                # embed.add_embed_field(name='Region', value='Southern California', inline=True)
                                # # embed.add_embed_field(name='Alert Status', value=no_cfa, inline=True)
                                # embed.set_image(url='https://i.pinimg.com/originals/c9/e6/2f/c9e62f19246adcaf9b64897be3d3bda0.gif')
                                # embed.set_footer(text='CA Chef Foodies',
                                #                  icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                                # embed.set_timestamp()
                                # webhook.add_embed(embed)
                                # response = webhook.execute()
                                # # print(convert_date, 'No CFA')
                                pass
                        else:
                            actual_score = int(score[0])
                            if actual_score >= runs:
                                # Discord Logic
                                embed = DiscordEmbed(title='Chick-Fil-A Sandwich Alert', description=cfa, color='FF0000')
                                # embed.set_thumbnail(url=image_link)
                                embed.add_embed_field(name='Date', value=game_date, inline=True)
                                embed.add_embed_field(name='Region', value='Southern California', inline=True)
                                # embed.add_embed_field(name='Alert Status', value=cfa, inline=True)
                                embed.set_image(url='https://i.pinimg.com/originals/c9/e6/2f/c9e62f19246adcaf9b64897be3d3bda0.gif')
                                embed.set_footer(text='CA Chef Foodies',
                                                 icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                                embed.set_timestamp()
                                webhook.add_embed(embed)
                                # response = webhook.execute()
                                # print(convert_date, 'CFA Sandwich Alert')
                            else:
                                # # Discord Logic
                                # embed = DiscordEmbed(title='Chick-Fil-A Sandwich Alert', color='FF0000')
                                # # embed.set_thumbnail(url=image_link)
                                # embed.add_embed_field(name='Date', value=game_date, inline=True)
                                # embed.add_embed_field(name='Alert Status', value=no_cfa, inline=True)
                                # embed.set_image(url='https://i.pinimg.com/originals/c9/e6/2f/c9e62f19246adcaf9b64897be3d3bda0.gif')
                                # embed.set_footer(text='CA Chef Foodies',
                                #                  icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                                # embed.set_timestamp()
                                # webhook.add_embed(embed)
                                # response = webhook.execute()
                                # # print(convert_date, 'No CFA Bottom')
                                pass

            except:
                pass

def cubs(cubs_url):
    page = requests.get(cubs_url)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table', class_='TableBase-table')

    no_cfa = "Chicago Cubs didn't win at home, no free sandwiches!"
    cfa = 'Chicago Cubs win! Check your app to redeem a free sandwich before 10:30AM CDT the following day!'

    for team in table.find_all('tbody'):
        rows = team.find_all('tr')
        for row in rows:
            try:
                game_date = row.find('td', class_='TableBase-bodyTd').text.strip()
                convert_date = datetime.strptime(game_date, '%b %d, %Y').date()
                home_game = row.find('span', class_='CellLogoNameLockup-opposingPrefix').text.strip()
                results = row.find('div', class_='CellGame').text.split(' ')[0]
                score = row.find('div', class_='CellGame').text.split(' ')[1].split('-')
                if convert_date == today:
                    if home_game != '@':
                        # runs = 7
                        # W = left number and L = right number
                        if results == 'W':
                            embed = DiscordEmbed(title='Chick-Fil-A Sandwich Alert', description=cfa, color='FF0000')
                            # embed.set_thumbnail(url=image_link)
                            embed.add_embed_field(name='Date', value=game_date, inline=True)
                            embed.add_embed_field(name='Region', value='Chicago', inline=True)
                            embed.set_image(
                                url='https://content.sportslogos.net/logos/54/54/full/wfumtjgnhk5dw395hpkfcwp7e.gif')
                            # embed.add_embed_field(name='Alert Status', value=cfa, inline=True)
                            embed.set_footer(text='Powered by CA Chef Foodies',
                                             icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                            embed.set_timestamp()
                            webhook.add_embed(embed)
                            # response = webhook.execute()
            except:
                pass

def dodgers(dodgers_url):
    page = requests.get(dodgers_url)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table', class_='TableBase-table')

    no_cpk = "Dodger's Lose! No free pizza from California Pizza Kitchen."
    cpk = "Dodger's Win! Check your California Pizza Kitchen rewards section to claim free 7 inch Pizza for Socal regions!"
    mcd = 'Free 6 piece McNuggets with a purchase of any small fry.'

    for team in table.find_all('tbody'):
        rows = team.find_all('tr')
        for row in rows:
            try:
                game_date = row.find('td', class_='TableBase-bodyTd').text.strip()
                convert_date = datetime.strptime(game_date, '%b %d, %Y').date()
                # print(convert_date)
                home_game = row.find('span', class_='CellLogoNameLockup-opposingPrefix').text.strip()
                results = row.find('div', class_='CellGame').text.split(' ')[0]
                score = row.find('div', class_='CellGame').text.split(' ')[1].split('-')
                if convert_date == today:
                    if home_game != '@':
                        # W = left number and L = right number
                        runs = 6
                        if results == 'W':
                            # Discord Logic
                            embed = DiscordEmbed(title='California Pizza Kitchen Alert', description=cpk, color='FF0000')
                            # embed.set_thumbnail(url=image_link)
                            embed.set_author(name='Foodie Bot', icon_url='https://images.getbento.com/accounts/8f224f281c0b0dc913515231c0f0fb7b/media/images/38208little_chef_logo_01.png')
                            embed.add_embed_field(name='Date', value=game_date, inline=True)
                            embed.add_embed_field(name='Region', value='Southern California', inline=True)
                            # embed.add_embed_field(name='Alert Status', value=cfa, inline=True)
                            embed.set_image(url='https://cdn.sanity.io/images/91ree6di/production/2e9b3c2e24e53d8fe4a59b30a972b05bbca1cee7-1140x400.png')
                            embed.set_footer(text='Powered by CA Chef Foodies',
                                             icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                            embed.set_timestamp()
                            webhook.add_embed(embed)
                            embed.add_embed_field(name='More Info', value='https://www.cpk.com/dodgers', inline=False)

                        actual_score = int(score[0])
                        if actual_score >= runs:
                            # Discord Logic
                            embed = DiscordEmbed(title='McDonalds Alert', description=mcd, color='FF0000')
                            # embed.set_thumbnail(url=image_link)
                            embed.add_embed_field(name='Date', value=game_date, inline=True)
                            embed.add_embed_field(name='Region', value='Southern California', inline=True)
                            # embed.add_embed_field(name='Alert Status', value=cfa, inline=True)
                            embed.set_image(
                                url='https://pbs.twimg.com/media/D71PauAXUAE5mYP?format=jpg&name=large')
                            embed.set_footer(text='CA Chef Foodies',
                                             icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                            embed.set_timestamp()
                            webhook.add_embed(embed)
                            # response = webhook.execute()
                        else:
                            pass

                            # Discord Logic for CFA
                        loss_score = int(score[1])
                        if loss_score >= runs:
                            # Discord Logic
                            embed = DiscordEmbed(title='McDonalds Alert', description=mcd, color='FF0000')
                            # embed.set_thumbnail(url=image_link)
                            embed.add_embed_field(name='Date', value=game_date, inline=True)
                            embed.add_embed_field(name='Region', value='Southern California', inline=True)
                            # embed.add_embed_field(name='Alert Status', value=cfa, inline=True)
                            embed.set_image(
                                url='https://pbs.twimg.com/media/D71PauAXUAE5mYP?format=jpg&name=large')
                            embed.set_footer(text='Powered by CA Chef Foodies',
                                             icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                            embed.set_timestamp()
                            webhook.add_embed(embed)
                            # response = webhook.execute()
                        else:
                            pass
            except:
                pass

#fix rockies, displaying 2 exectuions.
def rockies(rockies_url):
    page = requests.get(rockies_url)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table', class_='TableBase-table')

    no_tb = "Rockies didn't score more than 7 runs. No free sandwiches!"
    tb = 'Rockies scored more than 7 runs! \n\n From 4PM to 6PM local time, Taco Bell are offering four (4) regular crunchy tacos for $2. You must order four tacos to redeem the offer. \n\nThe offer is only valid in-restaurant at participating locations within the Denver metro area, not online or via any third-party delivery service. (The offer excludes any other tacos on the menu — only regular crunchy tacos.)'

    for team in table.find_all('tbody'):
        rows = team.find_all('tr')
        for row in rows:
            try:
                game_date = row.find('td', class_='TableBase-bodyTd').text.strip()
                convert_date = datetime.strptime(game_date, '%b %d, %Y').date()
                home_game = row.find('span', class_='CellLogoNameLockup-opposingPrefix').text.strip()
                results = row.find('div', class_='CellGame').text.split(' ')[0]
                score = row.find('div', class_='CellGame').text.split(' ')[1].split('-')
                if convert_date == today:
                        runs = 5
                        # W = left number and L = right number
                        if results == 'W':
                            actual_score = int(score[0])
                            print(actual_score)
                            if actual_score >= runs:
                                # Discord Logic
                                # print(actual_score)
                                embed = DiscordEmbed(title='Taco Bell Alert', description=tb, color='FF0000')
                                embed.add_embed_field(name='Date', value=game_date, inline=True)
                                embed.add_embed_field(name='Region', value='Denvor Metro Area', inline=True)
                                embed.set_image(url='https://pbs.twimg.com/media/CmnPWAsUMAA2d68.jpg')
                                embed.set_footer(text='CA Chef Foodies',
                                                 icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                                embed.set_timestamp()
                                webhook.add_embed(embed)
                                # response = webhook.execute()
                            else:
                                pass
                            # Discord Logic for CFA
                            # loss_score = int(score[1])
                            # actual_score = int(score[0])
                            # # print(loss_score)
                            # if actual_score >= runs:
                            #     # Discord Logic
                            #     embed = DiscordEmbed(title='Taco Bell Alert', description='The offer is only valid in-restaurant at participating locations within the Denver metro area, not online or via any third-party delivery service. (The offer excludes any other tacos on the menu — only regular crunchy tacos.) ' ,color='FF0000')
                            #     embed.add_embed_field(name='Date', value=game_date, inline=True)
                            #     embed.add_embed_field(name='Region', value='Denvor Metro Area', inline=True)
                            #     embed.add_embed_field(name='Alert Status', value=tb, inline=True)
                            #     embed.set_image(url='https://pbs.twimg.com/media/CmnPWAsUMAA2d68.jpg')
                            #     embed.set_footer(text='Powered by CA Chef Foodies',
                            #                      icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                            #     embed.set_timestamp()
                            #     webhook.add_embed(embed)
                            #     response = webhook.execute()
                            # else:
                            #     pass
                        else:
                            #Loss game. team score is left and oppononent score is right
                            loss_score = int(score[0])
                            print(loss_score)
                            if loss_score >= runs:
                                # Discord Logic
                                # print(actual_score)
                                embed = DiscordEmbed(title='Taco Bell Alert', description=tb, color='FF0000')
                                embed.add_embed_field(name='Date', value=game_date, inline=True)
                                embed.add_embed_field(name='Region', value='Denvor Metro Area', inline=True)
                                embed.set_image(url='https://pbs.twimg.com/media/CmnPWAsUMAA2d68.jpg')
                                embed.set_footer(text='CA Chef Foodies',
                                                 icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                                embed.set_timestamp()
                                webhook.add_embed(embed)
                                # response = webhook.execute()
                            else:
                                pass
                            # Discord Logic for CFA
                            # loss_score = int(score[1])
                            # loss_score = int(score[0])
                            # # print(loss_score)
                            # if loss_score >= runs:
                            #     # Discord Logic
                            #     embed = DiscordEmbed(title='Taco Bell Alert', description='The offer is only valid in-restaurant at participating locations within the Denver metro area, not online or via any third-party delivery service. (The offer excludes any other tacos on the menu — only regular crunchy tacos.) ' ,color='FF0000')
                            #     embed.add_embed_field(name='Date', value=game_date, inline=True)
                            #     embed.add_embed_field(name='Region', value='Denvor Metro Area', inline=True)
                            #     embed.add_embed_field(name='Alert Status', value=tb, inline=True)
                            #     embed.set_image(url='https://pbs.twimg.com/media/CmnPWAsUMAA2d68.jpg')
                            #     embed.set_footer(text='Powered by CA Chef Foodies',
                            #                      icon_url='http://hollywoodlife.com/wp-content/uploads/2019/01/geoff-hamanishi-kassandra-admits-to-cheating-ftr.jpg')
                            #     embed.set_timestamp()
                            #     webhook.add_embed(embed)
                            #     response = webhook.execute()
                            # else:
                            #     pass
            except:
                pass

cubs(cubs_url)
angels(angels_url)
dodgers(dodgers_url)
rockies(rockies_url)
response = webhook.execute()
