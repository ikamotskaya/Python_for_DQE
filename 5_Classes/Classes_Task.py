from datetime import datetime         # import datetime module for now()


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
    def __init__(self, title):
        """
        Constructor for News. Getting Text of News and City implemented as input from a console.
        """
        super().__init__(title)
        print('Input text of the news')
        self.text = input()
        print('Input city of the news')
        self.city = input()
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
    def __init__(self, title):
        """
        Constructor for Advertisement. Getting Text of Advertisement and Expiration Date implemented as input from a console.
        """
        super().__init__(title)
        print('Input text of the advertisement')
        self.text = input()
        print('Input expiration date DD/MM/YYYY')
        self.exp_date = input()
        self.__check_date()
        self.days_left = self.__get_day_left()

    def __check_date(self):
        """
        Check if the input date has a correct format DD/MM/YYYY
        """
        try:
            datetime.strptime(self.exp_date,'%d/%m/%Y')
        except:
            print('Incorrect input date, try again')    # if incorrect input print the message
            self.exp_date = input()                     # repeat the input
            self.__check_date()                         # check format again

    def __get_day_left(self):
        """
        Calculate how many days left to the expiration date.
        """
        return (datetime.now() - datetime.strptime(self.exp_date,'%d/%m/%Y')).days * (-1)

    def create_publication_str(self):
        """
        Return: str -->  return a str variable to write one to the file
        """
        return f'{self.title} \n{self.text} \nActual until: {self.exp_date},  {self.days_left} day{"s" if self.days_left != 1 else ""} left\n\n'


class Forecast(Publication):
    def __init__(self, title):
        """
        Constructor for Forecast. Getting Forecast City and Temperature implemented as input from a console.
        """
        super().__init__(title)
        print('Input city for forecast')
        self.city = input()
        print('Input forecast temperature')
        self.degree = input()
        self.__check_degree()
        self.feeling = self.__get_feeling()

    def __check_degree(self):
        """
        Check if the input value has an integer format
        """
        try:
            int(self.degree)
        except:
            print('Incorrect input temperature, try again')  # if incorrect input print the message
            self.degree = input()                       # repeat the input
            self.__check_degree()                       # check format again

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


def get_publication_by_type(pub_type):
    """
    Return: class object -->  return an corresponding class object according to the input parameter
    """
    if pub_type == '1':
        return News('News')
    elif pub_type == '2':
        return Advertisement('Private Ad')
    elif pub_type == '3':
        return Forecast('Forecast')


def is_valid_input(pub_type):
    """
    Check if the input is valid
    """
    return pub_type in ['1', '2', '3', '4']


def publish(publication):
    """
    Write publication str to file
    """
    with open('News feed', 'a+') as f:
        publication.title = publication.title.ljust(40, '-')
        f.write(publication.create_publication_str())


def main():
    pub_type = 1
    while pub_type != 4:
        print('What type of news do you want to generate? ')
        print('   1 - News\n   2 - Private advertisement\n   3 - Weather forecast   \n   4 - Exit')
        print('Input number ')
        pub_type = input()
        while not is_valid_input(pub_type):
            print('Incorrect input, try again')
            pub_type = input()
        if pub_type == '4':
            exit()
        publication = get_publication_by_type(pub_type)
        publish(publication)


if __name__ == "__main__":
    main()


