### Python Coding Script ###
### Topic-Based Content and Textual Analysis of Contemporary Political News Coverage
### Web-crawling: "Congress" section in Politico

import urllib.request, sys, time
from bs4 import BeautifulSoup
import requests
import csv

pagesToGet = 3258

upperframe = []
frame_health = []
frame_immigration = []
frame_social = []

Section_name = 'Congress'


for page in range(2, pagesToGet + 1):
    print('processing page :', page)
    url = 'https://www.politico.com/congress/' + str(page)
    print(url)

    ## An exception might be thrown, and therefore,
    try:
        # Use the browser to get the url
        page = requests.get(url)

    except Exception as e:  # This describes what to do if an exception is thrown
        error_type, error_obj, error_info = sys.exc_info()  # Get the exception information
        print('ERROR FOR LINK:', url)  # Print the link that cause the problem
        print(error_type, 'Line:', error_info.tb_lineno)  # Print error info and line that threw the exception
        continue  # Ignore this page. Abandon this and go back

    time.sleep(1)
    soup = BeautifulSoup(page.text, 'html.parser')

    links = soup.find_all('div', attrs = {'class': 'summary'})

    i = 0
    for itr in range(0,9):
        j = links[itr]
        Headline = j.find('h3').get_text().strip()

        if j.find('p', attrs = {'class':'byline'}) == None:
            continue
        elif j.find('p', attrs = {'class': 'timestamp'}) == None:
            continue
        else:
            Date = j.find('p', attrs = {'class': 'timestamp'}).get_text()
            Byline = j.find('p', attrs = {'class':'byline'}).get_text().strip()

    ## Web scraping the main news articles
            Link = j.find('h3').find("a")['href']

            try:
                page_article = requests.get(Link)

            except Exception as e:
                error_type, error_obj, error_info = sys.exc_info()
                print('ERROR FOR LINK:', Link)
                print(error_type, 'Line:', error_info.tb_lineno)
                continue

            time.sleep(1)
            soup_article = BeautifulSoup(page_article.text, 'html.parser')
            paragraphs = soup_article.find_all('p')

            Entire_article = []
            for para in paragraphs:
                para.get_text().strip()
                Entire_article.append(para.get_text().strip())

            Entire_article = ' '.join(Entire_article)

            if ('health care' in Entire_article) or ('healthcare' in Entire_article) or ('health insurance' in Entire_article) or ('health coverage' in Entire_article) or ('Medicare' in Entire_article)  or ('Medicaid' in Entire_article) or ('Veterans Health Administration' in Entire_article) or ('VHA' in Entire_article) or ('Military Health Service' in Entire_article) or ('MHS' in Entire_article):
                frame_health.append((Headline, Link, Date, Byline, Entire_article))
                print('keyword detected: healthcare')
                print(Headline + '___'+Link)
                print('--------')


                with open('Politico_'+str(Section_name)+'_healthcare.csv', 'w', encoding = 'UTF-8', newline = '') as out:
                    csv_out = csv.writer(out)
                    csv_out.writerow(['Head', 'Link', 'Date', 'Byline', 'Entire'])
                    for row in frame_health:
                        csv_out.writerow(row)
                out.close()

            if ('immigra' in Entire_article) and ('government' in Entire_article):
                frame_immigration.append((Headline, Link, Date, Byline, Entire_article))
                print('keyword detected: immigration')
                print(Headline + '___' + Link)
                print('--------')

                with open('Politico_'+str(Section_name)+'_immigration.csv', 'w', encoding = 'UTF-8', newline = '') as out:
                    csv_out = csv.writer(out)
                    csv_out.writerow(['Head', 'Link', 'Date', 'Byline', 'Entire'])
                    for row in frame_immigration:
                        csv_out.writerow(row)

            if ('social justice' in Entire_article) or ('racial justice' in Entire_article) or ('activism' in Entire_article) or ('protest' in Entire_article) or ('policing' in Entire_article) or ('demonstra' in Entire_article):
                frame_social.append((Headline, Link, Date, Byline, Entire_article))
                print('keyword detected: social injustice')
                print(Headline + '___'+Link)
                print('--------')

                with open('Politico_'+str(Section_name)+'_social_injustice.csv', 'w', encoding = 'UTF-8', newline = '') as out:
                    csv_out = csv.writer(out)
                    csv_out.writerow(['Head', 'Link', 'Date', 'Byline', 'Entire'])
                    for row in frame_social:
                        csv_out.writerow(row)
                out.close()
