import datetime as dt
from collections import Counter

from pep_parse.settings import BASE_DIR, DATETIME_FORMAT

statuses = []
results = ['Статус,Количество\n']


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
        for status, quantity in counter.items():
            results.append(f'{status},{quantity}\n')
        results.append(f'Total,{total}\n')
        self.file.writelines(results)
        self.file.close()
