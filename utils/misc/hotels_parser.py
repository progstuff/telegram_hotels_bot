class Hotel:
    def __init__(self):
        self.__id = 0
        self.__name = ''
        self.__address = ''
        self.__center_dist = ''

    def get_hotel_data(self, hotel):
        self.__id = hotel.get('id', None)
        self.__name = hotel.get('name', None)
        adr = hotel.get('address')
        if type(adr) is dict:
            self.__address = ', '.join([adr.get('locality', ''), adr.get('streetAddress', '')])
        landmarks = hotel.get('landmarks')
        if type(landmarks) is list:
            if landmarks[0].get('label', '') == 'City center':
                self.__center_dist = landmarks[0].get('distance', '')

    def get_str_view(self):
        rez = '\n'.join([self.__name, self.__address, self.__center_dist])
        return rez

