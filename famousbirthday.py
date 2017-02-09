from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

def scrape(url):
    content = urlopen(url).read()
    soup = BeautifulSoup(content, 'html.parser')
    celeb_data = soup.find_all('div', attrs={'class': 'info'})
    all_data = []   # list to store all data
    for item in celeb_data:
        celeb = item.find('div',attrs={'class': 'name'})
        prof = item.find('div',attrs={'class': 'title hidden-xs'})
            
        info = {}   # dictionary to store information about each person (name,age,profession,status)

        #filtering data
        if ',' in celeb.text:   # for alive
            celeb_list = celeb.text.split(',')
            celeb_name = celeb_list[0].strip()
            celeb_age = int(celeb_list[1].split()[0])
            info['Status'] = 'Alive'
        else:   # for dead
            celeb_list = celeb.text.split('(')
            celeb_name = celeb_list[0].strip()
            celeb_list[1] = celeb_list[1].replace(')', '')
            celeb_dob = celeb_list[1].split('-')[0]
            celeb_dod = celeb_list[1].split('-')[1]
            celeb_age = int(celeb_dod) - int(celeb_dob)
            info['Status'] = 'Dead'

        info['Name'] = celeb_name
        info['Age'] = celeb_age
        if prof:    # sometimes profession is absent
            celeb_profession = prof.text.strip()
            info['Profession'] = celeb_profession
        else:
            info['Profession'] = ''

        all_data.append(info)   # append dictionary to list

    return (all_data)

# save as csv
def save_to_csv(all_data, csv_file):
    headers = ['Name', 'Age', 'Profession', 'Status']
    with open(csv_file,'w') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(all_data)
    print("Saved to CSV successfully")
    
month = 'december'
day = '31'
url = 'http://www.famousbirthdays.com/' + month + day + '.html'
csv_file = month+day+'.csv'

birthday_list = scrape(url)
save_to_csv(birthday_list,csv_file)
