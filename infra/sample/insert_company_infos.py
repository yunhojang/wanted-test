import csv
import pymongo

if __name__ == "__main__":
    mongo_client = pymongo.MongoClient('mongodb://localhost:27017/wanted').get_default_database()
    TAGS = ['tag_ko', 'tag_en', 'tag_ja']
    dict_list = []
    dict_list_append = dict_list.append
    exception = None

    try:
        reader = csv.DictReader(open('wanted_temp_data.csv', 'r'))
        for line in reader:
            dict_list_append(line)

        for dict_ in dict_list:
            dict_['_cls'] = '__main__.CompanyInfo'
            for key, value in dict_.items():
                if key in TAGS:
                    dict_[key] = value.split('|')

        mongo_client['company_info'].create_index([
            ("$**", pymongo.TEXT)
        ])
        mongo_client['company_info'].insert_many(dict_list)
    except Exception as e:
        exception = e

    if exception is not None:
        with open("exceptions.log", "w") as f:
            f.write(str(exception))
