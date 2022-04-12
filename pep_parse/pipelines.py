import datetime as dt
from collections import Counter

from pep_parse.settings import BASE_DIR, DATETIME_FORMAT

statuses = []


class PepParsePipeline:

    def open_spider(self, spider):
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now_formatted}.csv'
        file_path = results_dir / file_name
        self.file = open(file_path, mode='w', encoding='utf-8')

    def process_item(self, item, spider):
        statuses.append(item['status'])
        return item

    def close_spider(self, spider):
        total = len(statuses)
        counter = Counter(statuses)
        self.file.write('Статус,Количество\n')
        for status, quantity in counter.items():
            self.file.write(f'{status},{quantity}\n')
        self.file.write(f'Total,{total}\n')
        self.file.close()
