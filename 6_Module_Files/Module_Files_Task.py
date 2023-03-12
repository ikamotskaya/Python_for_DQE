import os
import sys
from validation_utils import *


def format_row(inp_str, divide_symbol='|'):
    """
    Return list of normalised items from inp_str divided '|'. For example: ['1','Some news...','Minsk']
    """
    out_list = []
    for inp_str in inp_str.split(divide_symbol):
        inp_str = inp_str.lower().strip().capitalize()
        inp_str = inp_str.replace('\n', '').replace('\\n', '')
        out_list.append(inp_str)
    return out_list


class PublicationFile:
    """
    File has format one row - one publication divided by '|'. For example: '1|Some news...|Minsk'
    """
    def __init__(self, path='News.txt'):
        self.path = path
        self.text_from_file = []              # One list Item = an one text row from the file

    def read_file(self):
        """
        Return a list of str. One list Item = one text row from the file
        """
        with open(self.path, 'r') as f:
            self.text_from_file = [format_row(line) for line in f]
        print(self.text_from_file)
        self.is_valid_file()
        return self.text_from_file

    def is_valid_file(self):
        """
        Function validates if all data in the file correct.
        If invalid data presents in the file, the message will display and program execution will stop
        """
        for idx, line in enumerate(self.text_from_file):
            if not is_valid_pub_type(line[0]):
                print(f'Publication type in the row {idx+1} is incorrect')
                sys.exit()
            if line[0] == '2':
                if not is_valid_date(line[2]):
                    print(f'Date format in the row {idx+1} is incorrect')
                    sys.exit()
            if line[0] == '3':
                if not is_valid_degree(line[2]):
                    print(f'Degree format in the row {idx+1} is incorrect')
                    sys.exit()

    def del_file(self):
        """
        Function deletes the file
        """
        try:
            os.remove(self.path)
            print(f'The file {self.path} was successfully removed')
        except OSError as error:
            print(error)
            print(f'File {self.path} can not be removed')


class Publication:
    def __init__(self, title):
        self.title = title

    def create_publication_str(self):
        """
        Create publication string to write one to the file.
        The method has to be overridden in the child class.
        """
        pass


class News(Publication):
    def __init__(self, title, text, city):
        """
        Constructor for News. Getting Text of News and City implemented as input from a console.
        """
        super().__init__(title)
        self.text = text
        self.city = city
        self.date = self.__get_news_date()

    def __get_news_date(self):
        """
        Return: current_date: str -->  return a current date in the format DD/MM/YYYY HH.MM
        """
        current_date = datetime.now()
        current_date = current_date.strftime('%d/%m/%Y %H.%M')
        return current_date

    def create_publication_str(self):
        """
        Return: str -->  return a str variable to write one to the file
        """
        return f'{self.title} \n{self.text} \n{self.city}, {self.date}\n\n'


class Advertisement(Publication):
    def __init__(self, title, text, exp_date):
        """
        Constructor for Advertisement. Getting Text of Advertisement and Expiration Date implemented as input from a console.
        """
        super().__init__(title)
        self.text = text
        self.exp_date = exp_date.replace('\n','')
        self.days_left = self.__get_day_left()

    def __get_day_left(self):
        """
        Calculate how many days left to the expiration date.
        """
        return (datetime.now() - datetime.strptime(self.exp_date,'%d/%m/%Y')).days * (-1)

    def create_publication_str(self):
        """
        Return: str -->  return a str variable to write one to the file
        """
        publication_str = f'{self.title} \n{self.text} \nActual until: {self.exp_date},  ' \
                          f'{self.days_left} day{"s" if self.days_left != 1 else ""} left\n\n'
        return publication_str


class Forecast(Publication):
    def __init__(self, title, city, degree):
        """
        Constructor for Forecast. Getting Forecast City and Temperature implemented as input from a console.
        """
        super().__init__(title)
        self.city = city
        self.degree = degree
        self.feeling = self.__get_feeling()

    def __get_feeling(self):
        f = ''
        if int(self.degree) < 10:
            f = 'Cold'
        elif (int(self.degree) >= 10) and (int(self.degree) <= 28):
            f = 'Comfortable'
        elif int(self.degree) > 28:
            f = 'Hot'
        return f

    def create_publication_str(self):
        """
        Return: str -->  return a str variable to write one to the file
        """
        return f'{self.title} \n{self.city} \nTemperature: {self.degree},  {self.feeling}\n\n'


def get_publication_by_type(row):
    """
    Return: class object -->  return an corresponding class object according to the input parameter
    """
    pub_type = row[0]
    if pub_type == '1':
        return News('News', row[1], row[2])
    elif pub_type == '2':
        return Advertisement('Private Ad', row[1], row[2])
    elif pub_type == '3':
        return Forecast('Forecast', row[1], row[2])


def publish(publication):
    """
    Write publication str to the file
    """
    with open('News feed', 'a+') as f:
        publication.title = publication.title.ljust(40, '-')
        f.write(publication.create_publication_str())


def main():
    print('Input file for processing (by default ''News.txt'')\n')
    file_path = input() or 'News.txt'
    inp_file = PublicationFile(file_path)
    list_of_publications = inp_file.read_file()
    for pub in list_of_publications:
        publication = get_publication_by_type(pub)
        publish(publication)
    inp_file.del_file()


if __name__ == "__main__":
    main()

