from database.insert_or_update import insert_or_update


class MySQLStorePipeline:
    def process_item(self, item, spider):
        if not insert_or_update(item):
            return
        return item
