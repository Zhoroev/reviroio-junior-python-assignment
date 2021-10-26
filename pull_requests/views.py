from django.shortcuts import render
from django.views import View

import requests
from bs4 import BeautifulSoup

from pull_requests.forms import UserRequestForm
from pull_requests.models import UserRequest, UserRequestResult


class UserRequestView(View):

    def get(self, request):
        user_request_form = UserRequestForm
        return render(request, 'pull_requests/index.html', context={'user_request_form': user_request_form})

    def post(self, request):
        bound_form = UserRequestForm(request.POST)
        if bound_form.is_valid():
            link_github = bound_form.cleaned_data.get('link_github')
            user_req_link = UserRequest.objects.create(link_github=link_github)

            source = requests.get(link_github + '/pulls')
            soup = BeautifulSoup(source.text, "html.parser")
            ads = soup.find('div', class_='js-navigation-container js-active-navigation-container')
            if ads:
                ads = ads.find_all('div', class_='Box-row Box-row--focus-gray p-0 mt-0 js-navigation-item js-issue-row')
                for ad in ads:
                    link = 'https://github.com' + ad.\
                        find('div', class_='d-flex Box-row--drag-hide position-relative').\
                        find('a').get('href')

                    source2 = requests.get(link)
                    soup2 = BeautifulSoup(source2.text, "html.parser")

                    name = soup2.find('div', class_="js-check-all-container"). \
                        find_next('div', class_="gh-header-show"). \
                        find_next('div', class_="d-flex flex-column flex-md-row"). \
                        find_next('h1', class_="gh-header-title"). \
                        find('span', class_="js-issue-title markdown-title").text

                    reviewer = soup2.find('form', class_="js-issue-sidebar-form"). \
                        find('span', class_="css-truncate").find('p', class_="d-flex")
                    if reviewer:
                        reviewer = reviewer.\
                            find_next('span', class_="css-truncate-target width-fit v-align-middle").text
                    else:
                        reviewer = 'No reviews'

                    assignee = soup2.find('form', class_="js-issue-sidebar-form"). \
                        find_next('span', class_="css-truncate js-issue-assignees"). \
                        find_next('span', class_="css-truncate-target width-fit v-align-middle")
                    if assignee:
                        assignee = assignee.text
                    else:
                        assignee = 'No one assigned'

                    UserRequestResult.objects.create(name=name, reviewer=reviewer, assignee=assignee,
                                                     link=link, user_req_link=user_req_link)
            else:
                print('No Pull Requests')
        print('Success')
        return render(request, 'pull_requests/index.html', context={'user_request_form': bound_form,}, )


def user_request_result_view(request):
    user_request_results = UserRequestResult.objects.all()
    return render(request, 'pull_requests/index.html', context={'user_request_results': user_request_results, }, )