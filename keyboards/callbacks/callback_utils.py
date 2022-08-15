class CallbackAnswer:
    def return_answer(self) -> (bool, str):
        return False, ''


class BestDealCallbackAnswer(CallbackAnswer):
    def return_answer(self):
        return True, 'Загружаю отели с выбранными параметрами'


class HighPriceCallbackAnswer(CallbackAnswer):
    def return_answer(self):
        return True, 'Загружаю топ дорогих отелей'


class LowPriceCallbackAnswer(CallbackAnswer):
    def return_answer(self):
        return True, 'Загружаю топ бюджетных отелей'


class HistoryCallbackAnswer(CallbackAnswer):
    def return_answer(self):
        return True, 'Загружаю историю запросов'


class UnknownCallbackAnswer(CallbackAnswer):
    def return_answer(self):
        return False, 'Неизвестный запрос'


def get_answer_object(callback_data: str) -> CallbackAnswer:
    if callback_data == "lowprice":
        return LowPriceCallbackAnswer()
    elif callback_data == "highprice":
        return HighPriceCallbackAnswer()
    elif callback_data == "bestdeal":
        return BestDealCallbackAnswer()
    elif callback_data == "history":
        return HistoryCallbackAnswer()
    else:
        return UnknownCallbackAnswer()



