import requests
from bs4 import BeautifulSoup


def scraped_data(url):
    response = requests.get(url)
    data = BeautifulSoup(response.text, 'html.parser')
    return data


def improved_query(query):
    new_query = ''
    for i in query:
        if i == ' ':
            new_query += '+'
        else:
            new_query += i
    return new_query


def fix_text(text, flag=False):
    if text == '' or text == '\n':
        return ''
    i = 0
    while text[i] == ' ' or text[i] == '\n':
        i += 1
    text = text[i:]
    while text[-1] == ' ' or text[-1] == '\n':
        text = text[:-1]
    i = 0
    if '/' in text:
        text = text[:text.index('/')-1]

    if flag:
        num = [str(i) for i in range(0, 10)]
        for i in range(len(text)):
            if text[i] in num:
                text = text[1:i-1]
                break
        new_text = ''
        for i in text:
            if i != '\n': new_text += i
        text = new_text
    return text


class IMDB:
    def __init__(self, query):
        try:
            self.display_flag = True
            query = improved_query(query)
            url = 'https://www.imdb.com/find?q=' + query
            data = scraped_data(url)

            imdb_title = data.find(class_='result_text').find('a')
            # title
            self.title = imdb_title.get_text()

            imdb_link = imdb_title['href']
            url = 'https://www.imdb.com' + imdb_link
            data = scraped_data(url)

            # genre
            try:
	            self.genre = [i.get_text() for i in data.find(
	            	class_='subtext').find_all('a')[:-1]]
            except:
            	self.genre = False
            # imdb
            try:
	            self.imdb = data.find(
	                attrs={'itemprop': 'ratingValue'}).get_text()
            except:
            	self.imdb = False
            # release date
            try:
	            self.date = data.find(
	                attrs={'title': 'See more release dates'}).get_text()[:-1]
            except:
            	self.date = False
            try:
            	self.summary = data.find(class_='summary_text').get_text()
            	cast_data = data.find(class_='cast_list').find_all('tr')[1:]
            except:
            	self.summary = False

            # synopsis
            self.summary = fix_text(self.summary)
            # cast
            self.cast = {}
            try:
                arr = ['', 'odd', 'even']
                flag = 1
                for roles in cast_data:
                    if roles['class'][0] == arr[flag]:
                        actor = roles.find_all('a')[1].get_text()[1:-1]
                        character = fix_text(roles.find(
                            class_='character').get_text(), True)
                        self.cast[actor] = character
                        flag *= -1
            except:
                pass
        except:
            self.display_flag = False
            print('No results found.')

    def __repr__(self):
        try:
            return f'This object contain details about \'{self.title}\'.'
        except:
            return 'No information available.'

    def display(self):
        if self.display_flag:
            try:
                if self.title: print(f'\nTitle - {self.title}')
                if self.imdb: print(f'\nIMDB - {self.imdb}')
                if self.genre: print(f'Genre - {self.genre}')
                if self.date: print(f'Date - {self.date}')
                if self.summary: print(f'\n{self.summary}\n')

                for actor in self.cast:
                    character = self.cast[actor]
                    if character == '':
                        print(actor)
                    else:
                        print(actor + ' - ' + character)
                print()
            except:
                pass
