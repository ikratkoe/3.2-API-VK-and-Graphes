import requests
import networkx as nx
import matplotlib.pyplot as plt


AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.63'
APP_ID = 5940629  # Your app_id here


def get_frnd_list(id):
    # response = requests.get('https://api.vk.com/method/status.get', {'user_id':id})
    # print(response.json())
    params = {
        'user_id': id,
        'version': VERSION
    }
    if not(is_activ_user_get(id)) :
        return []
    response = requests.get('https://api.vk.com/method/friends.get', params)
    friends = response.json()['response']
    return friends

def is_activ_user_get(id):              # проверка на бан пользователя по id
    params = {
        'user_id': id,
        'version': VERSION
    }
    response = requests.get('https://api.vk.com/method/users.get', params)
    resp = response.json()
    return (0 if 'deactivated' in resp['response'][0] else  1)


def draw_edges(id , nds):             # рисуем грани от центра
    edges = [(id,x) for x in nds ]
    G.add_edges_from(edges)



ban = 0       #  количество моих друзей забаненных VK
id = 1071928
    # 942789

my_friends = get_frnd_list(id)
print("У вас  {}  друзей: {}".format(len(my_friends), my_friends))

G = nx.Graph()
G.add_node(id)
G.add_nodes_from(my_friends)
draw_edges(id, my_friends)

list_frds = []
for id in my_friends:
    frs = get_frnd_list(id)
    if frs == [] :
        ban +=1
    else:
        print("id  {} имеет {} друзей".format(id, len(frs)))
        list_frds.extend(frs)
        draw_edges(id, frs)

print("Общее количество друзей-друзей = ", len(list_frds))

list_frds.sort()
dict_frds = {}
cnt = 0              # количество пересечений друзей
for i in range(len(list_frds)):
    if i > 0 and list_frds[i] == list_frds[i-1] :    # цепочка тянется
        cnt +=1
        continue
    elif i > 0 and list_frds[i] != list_frds[i-1] and cnt > 0 :   # одинаковая цепочка кончилась , фиксируем
        dict_frds[i] = cnt+1    # количество общих друзей
        cnt = 0
        continue

print("У вас ", ban, " забаненных VK друзей")
print(" Всего популярных друзей друзей :" , len(dict_frds)  )

# по приколу сортируем вывод по убыванию популярности
print("(id, популярность)",sorted(dict_frds.items(), key=lambda x: x[1], reverse=True) )



nx.draw(G)
plt.show()

