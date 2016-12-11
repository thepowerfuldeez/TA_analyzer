import vk_api
import pickle
from sklearn.metrics.pairwise import cosine_similarity


class Analyzer:
    
    def __init__(self, token="4ee251bf489b9d88106f08b36239eb0ab39bed07ca3fb9adacf62346cb2981eed59a26f4c29a18123f053"):
        vk_session = vk_api.VkApi(token)
        vk_session.authorization()
        cached_ids = pickle.load(open("cache.p", "rb"))
        vector_cache = pickle.load(open("vector_cache.p", "rb"))
    
    def to_cache(self, input_):
        global cached_ids

        shortname = group_link[group_link.rfind("/")+1:]
        if "public" in shortname:
            shortname = shortname[6:]
        print(group_link)

        r = vk_session.method("groups.getById", {"group_ids": shortname})
        group_id = r[0]["id"]

        if group_id not in self.cached_ids.keys():

            """Все сообщества подписчиков сообщества"""
            users = vk_api.VkTools(vk_session).get_all("groups.getMembers", 100, {'group_id':group_id})['items']
            k = int(len(users) / 1000)
            if k:
                users = users[::k]

            data_for_clustering = []
            users_publicpages = []
            with vk_api.VkRequestsPool(vk_session) as pool:

                for i in range(0, len(users), 1000):
                    batch = users[i:i+1000]
                    data_for_clustering.append(pool.method('users.get', {
                            "user_ids": batch,
                            "fields": "sex,age,education,universities,schools,interests,music,movies,bdate,city,country"
                        }))

                    for user_id in batch[:5]:
                        users_publicpages.append(pool.method('users.getSubscriptions', {
                                    "user_id": user_id
                                }))

            data_for_clustering = [x for x in [x.result for x in data_for_clustering]]
            t = []
            for user in users_publicpages:
                try:
                    t.append(user.result['groups']['items'])
                except:
                    pass
            users_publicpages = t

            wall50 = vk_session.method("wall.get", {"owner_id": -group_id, "filter": "owner", "count": 100})['items'][::2]

            result = data_for_clustering, users_publicpages, wall50
            self.cached_ids[group_id] = result
            pickle.dump(self.cached_ids, open("cache.p", "wb"))
            return self.from_cache(group_id)
        else:
            return self.from_cache(group_id)
    
    
    def from_cache(self, gid):
        global vector_cache
        
        x_0 = []
        try:
            for i in range(1000):
                x = self.cached_ids[gid][0][0][i]
                try:
                    ci = x["city"]["id"]
                except:
                    ci = 0
                try:
                    u = x["universities"][0]["id"]
                except:
                    u = 0
                try:
                    s = x["schools"][0]["id"]
                except:
                    s = 0
                try:
                    bd = x["bdate"]
                    if len(bd.split(".")) == 3:
                        age = 2014 - int(bd.split(".")[2])
                except:
                    age = 0
                x_0.append(np.array([x.get("sex", 0), ci, u, s, age], dtype="int32"))
            z_0 = []
            try:
                for j in range(50):
                    wall_post = self.cached_ids[gid][2][j]
                    has_photo, has_text, has_audio = 0, 0, 0
                    if wall_post.get("text"):
                        has_text = 1
                    t = wall_post.get("attachments")
                    if t:
                        for a in t:
                            if a.get("type") == "audio":
                                has_audio = 1
                            if a.get("type") == "photo":
                                has_photo = 1
                    z_0.append([has_text, has_photo, has_audio])
            except IndexError as e:
                print(e)

            t_sex = [z[0] for z in x_0]
            f1 = t_sex.count(2) / len(t_sex)
            f2 = t_sex.count(1) / len(t_sex)
            f3 = Counter([z[1] for z in x_0 if z[1]]).most_common(1)[0][0]
            f4 = Counter([z[2] for z in x_0 if z[2]]).most_common(1)[0][0]
            f5 = Counter([z[3] for z in x_0 if z[3]]).most_common(1)[0][0]
    #         f6_10 = [t[0] for t in Counter([item for sublist in cached_ids[gid][1] for item in sublist]).most_common(5)]
            f6_10 = [0, 0, 0, 0, 0]
            try:
                f11 = sum([z[0] for z in z_0]) / len(z_0)
            except:
                f11 = 0
            try:
                f12 = sum([z[1] for z in z_0]) / len(z_0)
            except:
                f12 = 0
            try:
                f13 = sum([z[2] for z in z_0]) / len(z_0)
            except:
                f13 = 0
            ages = [z[4] for z in x_0 if z[4]]
            f14 = np.median(ages)
            x_1 = [f1, f2, f3, f4, f5, *f6_10, f11, f12, f13, f14]
            
            result = np.array(x_1, dtype="float32")
            self.vector_cache[gid] = result
            pickle.dump(self.vector_cache, open("vector_cache.p", "wb"))
            return result
        except IndexError as e:
            print(e)
            
    def get_info(self, input_):
        vector = self.to_cache(input_)
        similarities = []
        for gid, other_vector in vector_cache.items():
            similarities.append([gid, cosine_similarity(vector, other_vector)[0]])
        return vector, sorted(similarities, reverse=True, key=lambda x: x[1])[:3]
        