import os
import sys
from validation_utils import *
import json
import xml.etree.ElementTree as ET
import pyodbc


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
    def __init__(self, path='News.txt'):
        self.path = path
        self.text_from_file = []
        self.dict_from_json = {}

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

    def is_valid_file(self):
        """
        Function validates if all data in the file correct.
        If invalid data presents in the file, the message will display and program execution will stop
        """
        for idx, line in enumerate(self.text_from_file):
            if not is_valid_pub_type(line[0]):
                print(f'Publication type in the {idx+1} publication is incorrect')
                sys.exit()
            if line[0] == '2':
                if not is_valid_date(line[2]):
                    print(f'Date format in the {idx+1} publication is incorrect')
                    sys.exit()
            if line[0] == '3':
                if not is_valid_degree(line[2]):
                    print(f'Degree format in the {idx+1} publication is incorrect')
                    sys.exit()


class PublicationTxtFile(PublicationFile):
    """
    File has format one row - one publication divided by '|'. For example: '1|Some news...|Minsk'
    """
    def read_file(self):
        """
        Return a list of str. One list Item = one text row from the file
        """
        with open(self.path, 'r') as f:
            self.text_from_file = [format_row(line) for line in f]
        print(self.text_from_file)
        self.is_valid_file()
        return self.text_from_file


class PublicationJSONFile(PublicationFile):
    """
    File has format {
                        "publication": [
                            {
                               "type": "1",
                                "text": "Some news ...",
                                "city": "Minsk"
                            },
                            {
                                "type": "2",
                                "text": "Some text of adv ...",
                                "exp_date": "23/03/2023"
                            },
                            {
                                "type": "3",
                                "city": "Minsk",
                                "degree": "-10"
                            }
                        ]
                    }
    """
    def read_file(self):
        """
        Return a list of lists. One internal list Item = one publication from the file
        """
        with open(self.path, 'r') as f:
            self.dict_from_json = json.load(f)
        for i in self.dict_from_json['publication']:
            pass # print(i)
        self.is_valid_file()
        text_from_file = []
        l = []
        for publ in self.dict_from_json['publication']:
            for v in publ.values():
                l.append(v)
            text_from_file.append(l)
            l = []
        return text_from_file

    def is_valid_file(self):
        """
        Function validates if all data in the file correct.
        If invalid data presents in the file, the message will display and program execution will stop
        """
        for publ in self.dict_from_json['publication']:
            for k, v in publ.items():
                if k == 'type':
                    if not is_valid_pub_type(v):
                        print(f'Publication type {v} is incorrect')
                        sys.exit()
                if k == 'exp_date':
                    if not is_valid_date(v):
                        print(f'Format of the date {v} is incorrect')
                        sys.exit()
                if k == 'degree':
                    if not is_valid_degree(v):
                        print(f'Degree format {v} is incorrect')
                        sys.exit()


class PublicationXMLFile(PublicationFile):
    """
       <publication>
            <type name="News">
                <text>Some news</text>
                <city>London</city>
            </type>
            <type name="Private Ad">
                <text>Get started with free personalised support. Create your custom ad plan with a Google Ads Expert.</text>
                <exp_date>23/04/2023</exp_date>
            </type>
            <type name="Forecast">
                <city>Barcelona</city>
                <degree>5</degree>
            </type>
        </publication>
    """
    def read_file(self):
        """
        Return a list of lists. One internal list Item = one publication from the file
        """
        xml_file = ET.parse(self.path)
        root = xml_file.getroot()
        for i in root.iter():
            if i.get('name') == 'News':
                text = i.find('text').text
                city = i.find('city').text
                self.text_from_file.append(['1', text, city])
            if i.get('name') == 'Private Ad':
                text = i.find('text').text
                exp_date = i.find('exp_date').text
                self.text_from_file.append(['2', text, exp_date])
            if i.get('name') == 'Forecast':
                city = i.find('city').text
                degree = i.find('degree').text
                self.text_from_file.append(['3', city, degree])
        return self.text_from_file


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
        self.table = 'news'

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

    def get_value_to_db(self):
        return [self.text, self.city, self.date]

    def get_fields_to_db(self):
        return ['text', 'city', 'date']


class Advertisement(Publication):
    def __init__(self, title, text, exp_date):
        """
        Constructor for Advertisement. Getting Text of Advertisement and Expiration Date implemented as input from a console.
        """
        super().__init__(title)
        self.text = text
        self.exp_date = exp_date.replace('\n','')
        self.days_left = self.__get_day_left()
        self.table = 'advertisement'

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

    def get_value_to_db(self):
        return [self.text,self.exp_date,self.days_left]

    def get_fields_to_db(self):
        return ['text', 'exp_date', 'days_left']


class Forecast(Publication):
    def __init__(self, title, city, degree):
        """
        Constructor for Forecast. Getting Forecast City and Temperature implemented as input from a console.
        """
        super().__init__(title)
        self.city = city
        self.degree = degree
        self.feeling = self.__get_feeling()
        self.table = 'forecast'

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

    def get_value_to_db(self):
        return [self.city, self.degree, self.feeling]

    def get_fields_to_db(self):
        return ['city', 'degree', 'feeling']


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


def input_type_file():
    print("Select the type of input file \n\t1 - txt, \n\t2 - json, \n\t3 - xml")
    t = int(input())
    if t in [1, 2, 3]:
        return t
    else:
        print('Incorrect input, try again')
        input_type_file()


def output_type():
    print("The processing result will write to \n\t1 - file 'Neews feed' \n\t2 - Database" )
    t = int(input())
    if t in [1, 2]:
        return t
    else:
        print('Incorrect input, try again')
        output_type()
    return int(input())


class DBConnection:
    def __init__(self, database):
        self.database = database
        with pyodbc.connect("DRIVER={SQLite3 ODBC Driver};"
                            "Direct=True;"
                            f"Database={self.database};"
                            "autocommit=True") as self.connection:
            with self.connection.cursor() as self.cur:
                self.cur.execute("CREATE TABLE IF NOT EXISTS news (text text, city text, date text)")
                self.cur.execute("CREATE TABLE IF NOT EXISTS advertisement (text text, exp_date text, days_left text)")
                self.cur.execute("CREATE TABLE IF NOT EXISTS forecast (city text, degree text, feeling text)")

    def insert(self, table, list_values):
        self.cur.execute(f"INSERT INTO {table} VALUES {tuple(list_values)}")
        self.cur.commit()

    def select(self, table, list_fields, list_values):
        str_fields = ','.join(list_fields)
        print('list_fields ', list_fields)
        sql = f"SELECT {str_fields} FROM {table} WHERE {list_fields[0]} = '{list_values[0]}' " \
              f"AND {list_fields[1]} = '{list_values[1]}' " \
              f"AND {list_fields[2]} = '{list_values[2]}'"
        print(sql)
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r is None:
            return True
        else:
            return False


def main():
    file_type = input_type_file()
    if file_type == 1:
        path = 'News.txt'
        print(f'Input file for processing (by default {path})\n')
        file_path = input() or path
        inp_file = PublicationTxtFile(file_path)
    elif file_type == 2:
        path = 'News.json'
        print(f'Input file for processing (by default {path})\n')
        file_path = input() or path
        inp_file = PublicationJSONFile(file_path)
    elif file_type == 3:
        path = 'News.xml'
        print(f'Input file for processing (by default {path})\n')
        file_path = input() or path
        inp_file = PublicationXMLFile(file_path)

    out_type = output_type()
    if out_type == 2:
        list_of_publications = inp_file.read_file()
        for pub in list_of_publications:
            publication = get_publication_by_type(pub)
            db = DBConnection('publications.db')
            if db.select(publication.table, publication.get_fields_to_db(), publication.get_value_to_db()):
                db.insert(publication.table, publication.get_value_to_db())
    else:
        list_of_publications = inp_file.read_file()
        for pub in list_of_publications:
            publication = get_publication_by_type(pub)
            publish(publication)
        inp_file.del_file()


if __name__ == "__main__":
    main()

