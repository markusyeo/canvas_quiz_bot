import requests
import dataclasses

from functools import lru_cache

@dataclasses.dataclass
class Table:
    headers: list
    data: list
    meta: dict = dataclasses.field(default_factory=dict)

    @property
    @lru_cache(maxsize=1)
    def df(self):
        import pandas as pd
        try:
            return pd.DataFrame(self.data, columns=self.headers)
        except:
            return None

    def to_csv(self, filename):
        import csv
        with open(filename, 'w', encoding='utf-8', newline='') as out:
            writer = csv.writer(out)
            writer.writerow(self.headers)
            writer.writerows(self.data)

    def __repr__(self):
        return self.df.to_string(index=False)

    def __hash__(self):
        return id(self)

class Rooted:
    def __init__(self, root, id=None, skip_url=False):
        self.root = root
        self.skip_url = skip_url
        if id is not None:
            self.id = id
            self.URL = root.URL + f'/{id}'

    def __getattribute__(self, name):
        try:
            result = super().__getattribute__(name)
            if name[:3] == 'URL':
                root = self.root.root if self.skip_url else self.root
                if result[:len(root.URL)] != root.URL:
                    return root.URL + '/' + result
        except AttributeError:
            result = self.root.__getattribute__(name)
        return result

    @property
    def name_to_id(self):
        return {row[1]: row[0] for row in self.info.data}

    def flush_cache(self):
        try:
            self.__class__.info.fget.cache_clear()
            self.__class__.stats.fget.cache_clear()
        except AttributeError:
            pass
        except Exception as e:
            print("error while clearing cache", e)

class CanvasHTTP(Rooted):
    VALID_STATUS_CODES = {200, 201, 202, 302}

    def __init__(self, root):
        self.session = requests.Session()
        super().__init__(root)

    def get(self, url, data=None, **kwargs):
        response = self.session.get(url, data=data, **kwargs)
        return self.with_warning(response)

    def post(self, url, data, tag=None, **kwargs):
        response = self.session.post(url, data=data, **kwargs)
        return self.with_warning(response)

    def patch(self, url, data, **kwargs):
        response = self.session.patch(url, data=data, **kwargs)
        return self.with_warning(response)

    def put(self, url, data, **kwargs):
        response = self.session.put(url, data=data, **kwargs)
        return self.with_warning(response)

    def delete(self, url, data=None, **kwargs):
        response = self.session.delete(url, data=data, **kwargs)
        return self.with_warning(response)

    @staticmethod
    def with_warning(response):
        if response.status_code not in CanvasHTTP.VALID_STATUS_CODES:
            print("WARNING! Invalid status code:", response.status_code, response.url)
        return response

def guess_id(getter):
    def guesser(self, *args, **kwargs):
        if 'id' in kwargs:
            return getter(self, id=kwargs.pop('id'))
        if args and type(args[0]) == int:
            return getter(self, id=args[0])
        if 'name' in kwargs and kwargs['name'] in self.name_to_id:
            return getter(self, id=self.name_to_id[kwargs.pop('name')])
        if args and args[0] in self.name_to_id:
            return getter(self, id=self.name_to_id[args[0]])
        if args and args[0] in self.name_to_id.values():
            return getter(self, id=args[0])
        raise Exception(f"Given `id` or `name` does not exist: {args if args else ''}{kwargs if kwargs else ''}")
    return guesser