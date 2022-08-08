from test_utils import TestQuerries

if __name__ == '__main__':
    test_querries = TestQuerries()
    print('Ответ от rapidapi:', test_querries.try_get_data_from_rapid())
    print('Ответ от бота:', test_querries.try_get_data_from_bot())
    pass
