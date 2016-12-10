import vk_api
import os
import time


class Vk:
    def __init__(self):
        """Авторизация ВКонтакте, инициализация сессии и инструментов"""
        session = vk_api.VkApi(os.environ['VK_LOGIN'], os.environ['VK_PASSWORD'], app_id=5559651)
        try:
            session.authorization()
        except vk_api.AuthorizationError as error_msg:
            print(error_msg)
        self.session = session
        self.tools = vk_api.VkTools(session)
        self.pool = vk_api.VkRequestsPool(session)

    def method(self, method_name, params=None):
        """Интерфейс обращения к методам ВКонтакте"""
        if params is None:
            params = {}
        try:
            return self.session.method(method_name, params)
        except Exception as msg:
            print(msg)
            return None

    def get_all(self, method_name, params=None):
        """Позволяет осуществлять в 25 раз больше запросов (идеально для выкачиваня стены)
        Работает только с методами, которые отдают count и items или users"""
        if params is None:
            params = {}
        try:
            return self.tools.get_all(method_name, 100, params)
        except Exception as msg:
            print(msg)
            return None


class Finder:
    """Позволяет найти человека по имени, дате рождения(если есть) или группам(если есть) ВКонтакте
    Возвращает ссылку на профиль, пол, дату рождения"""

    def __init__(self, groups=()):
        """
        Инициализация поиска по группам(если заданы) либо просто по ВКонтакте
        Вернет человека, только если результатов поиска будет не более 5
        """
        t = time.time()
        self.vk = Vk()
        self.users = set()
        for group_id in groups:
            try:
                self.users |= set([a.get('domain') for a in self.vk.get_all("groups.getMembers", {
                    "group_id": group_id,
                    "fields": "domain"
                })['items']])
            except:
                pass
        print("Initialization took {:.3f} seconds.".format(time.time() - t))

    def find(self, name, bdate=None) -> tuple():
        """Принимает имя пользователя, дату рождения в формате dd.mm.yyyy
        Возвращает ссылку на профиль, пол, дату рождения"""
        bd, bm, by = None, None, None
        if bdate:
            try:
                a = [int(t) for t in bdate.split(".")]
                bd = a[0]
                bm = a[1]
                by = a[2]
            except:
                pass
        finded_users = self.vk.get_all('users.search', {
            'q': name,
            'birth_day': bd,
            'birth_month': bm,
            'birth_year': by,
            'sort': 1,
            'fields': 'sex, bdate, domain'
        })
        domains = {a.get('domain'): (a.get('sex'), a.get('bdate')) for a in finded_users['items']}
        t = set(domains.keys()) & self.users

        if t:
            domain = next(iter(t))
        else:
            if not finded_users.get('count') > 5:
                return None
            else:
                domain = finded_users.get('items')[0].get('domain')

        s, bdate = domains[domain]
        if s == 1:
            sex = "Женщина"
        elif s == 2:
            sex = "Мужчина"
        else:
            sex = None

        return "https://vk.com/{}".format(domain), sex, bdate
