from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

keyboard_start1 = InlineKeyboardMarkup()
keyboard_start1.add(InlineKeyboardButton('Благодарственное письмо с полезностями', url='https://disk.yandex.ru/i/vLfCvB3aDAmvOA'))

keyboard_start2 = InlineKeyboardMarkup(row_width = 2)
keyboard_start2.insert(InlineKeyboardButton(text = 'Я был на встрече!', callback_data = 'iwasonmeeting'))
keyboard_start2.insert(InlineKeyboardButton(text = 'Я жду запись!', callback_data = 'iamwaitingforrecord'))

keyboard_iwasonmeeting = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True, row_width = 2)
keyboard_iwasonmeeting.insert(KeyboardButton('Это точно! Надо чаще встречаться!'))
keyboard_iwasonmeeting.insert(KeyboardButton('И в запись посмотреть тоже неплохо!'))

keyboard_ready = InlineKeyboardMarkup()
keyboard_ready.add(InlineKeyboardButton(text = 'Готово!', callback_data = 'check_ready'))

keyboard_iamwaitingrecord = InlineKeyboardMarkup()
keyboard_iamwaitingrecord.add(InlineKeyboardButton(text = 'Урааа!', callback_data = 'yay'))

keyboard_get_sub1 = InlineKeyboardMarkup()
keyboard_get_sub1.add(InlineKeyboardButton('Смотреть видеозапись бизнес-завтрака', url='https://www.youtube.com/watch?v=CsHLjdgYYWE&feature=youtu.be'))

keyboard_get_sub3 = InlineKeyboardMarkup()
keyboard_get_sub3.add(InlineKeyboardButton('Забирай про сценарии показа', url='https://disk.yandex.ru/i/IM1vfddQwm2C2g')).add(InlineKeyboardButton('А тут бланк аудита', url = 'https://disk.yandex.ru/i/jKm04SFPQRReWQ'))

keyboard_get_sub4 = InlineKeyboardMarkup()
keyboard_get_sub4.add(InlineKeyboardButton('Написать отзыв', url='https://docs.google.com/forms/d/1QvF7491yq1t7pAYQ2lZkucvv2G0Hp0d01_kBCOMqPmQ/viewform?edit_requested=true#responses'))

