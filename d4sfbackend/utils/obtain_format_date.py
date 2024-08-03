from datetime import datetime

class obtain_format_date():
    def year_eng():
        return str(datetime.today().strftime('%Y_%m_%d'))

