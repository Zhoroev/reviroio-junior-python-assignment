import requests
from bs4 import BeautifulSoup
link_github = 'https://github.com/kubernetes/kubernetes'
source = requests.get(link_github + '/pulls')
soup = BeautifulSoup(source.text, "html.parser")
ads = soup.find('div', class_='js-navigation-container js-active-navigation-container')
if ads:
    ads = ads.find_all('div', class_='Box-row Box-row--focus-gray p-0 mt-0 js-navigation-item js-issue-row')
    for ad in ads:
        link = 'https://github.com' + ad.find('div', class_='d-flex Box-row--drag-hide position-relative').find(
            'a').get('href')
        print(link)
        source2 = requests.get(link)
        soup2 = BeautifulSoup(source2.text, "html.parser")
        name = soup2.find('div', class_="js-check-all-container").\
            find_next('div', class_="gh-header-show").\
            find_next('div', class_="d-flex flex-column flex-md-row").\
            find_next('h1', class_="gh-header-title").\
            find('span', class_="js-issue-title markdown-title").text
        reviewer = soup2.find('form', class_="js-issue-sidebar-form").\
            find('span', class_="css-truncate").find('p', class_="d-flex")
        if reviewer:
            reviewer = reviewer.find_next('span', class_="css-truncate-target width-fit v-align-middle").text
        else:
            reviewer = 'No reviews'
        assignee = soup2.find('form', class_="js-issue-sidebar-form"). \
            find_next('span', class_="css-truncate js-issue-assignees"). \
            find_next('span', class_="css-truncate-target width-fit v-align-middle")
        if assignee:
            assignee = assignee.text
        else:
            assignee = 'No one assigned'
        print(reviewer, assignee)
else:
    print('No Pull Requests')
