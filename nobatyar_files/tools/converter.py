from persiantools import digits


# این کلاس ورودی‌های کاربر را (حتی اگر با ارقام فارسی نوشته شده باشند) به عدد انگلیسی تبدیل می کند
class Converter:
    @staticmethod
    def to_english(text):
        return digits.fa_to_en(digits.ar_to_fa(str(text))).strip()

    @staticmethod
    def to_int(text):
        try:
            return int(Converter.to_english(text))
        except ValueError:
            raise ValueError("مقدار عددی نامعتبر است")

    @staticmethod
    def to_int_list(text):
        text = Converter.to_english(text).replace("،", ",")
        number_list = []
        for item in text.split(","):
            if item.strip() != "":
                number = Converter.to_int(item)
                if number not in number_list:
                    number_list.append(number)
        return number_list
