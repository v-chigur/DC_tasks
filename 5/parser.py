import csv
import requests
from bs4 import BeautifulSoup

link = 'http://notelections.online/region/region/st-petersburg?action=show&root=1&tvd=27820001217417&vrn=27820001217413&region=78&global=&sub_region=78&prver=0&pronetvd=null&vibid=27820001217417&type=222'

columns = [['tik_name',
            'uik_name',
            'Число избирателей, внесенных в список избирателей на момент окончания голосования',
            'Число избирательных бюллетеней, полученных участковой избирательной комиссией',
            'Число избирательных бюллетеней, выданных избирателям в помещении для голосования в день голосования',
            'Число избирательных бюллетеней, выданных избирателям, проголосовавшим вне помещения для голосования',
            'Число погашенных избирательных бюллетеней',
            'Число избирательных бюллетеней, содержащихся в переносных ящиках для голосования',
            'Число избирательных бюллетеней, содержащихся в стационарных ящиках для голосования',
            'Число недействительных избирательных бюллетеней',
            'Число действительных избирательных бюллетеней',
            'Число утраченных избирательных бюллетеней',
            'Число избирательных бюллетеней, не учтенных при получении',
            'Амосов Михаил Иванович',
            'Беглов Александр Дмитриевич',
            'Тихонова Надежда Геннадьевна']]

html = requests.get(link)
parsed_html = BeautifulSoup(html.text, 'html.parser')

options_tags = parsed_html.find_all('option')[1:]

for i in range(len(options_tags)):
    options_tag = options_tags[i]

    parsed_option = BeautifulSoup(requests.get('http://notelections.online/region' + options_tag.get('value')).text, 'html.parser')

    tik_data = parsed_option.find_all('tr')[32:48]
    tik_data_uiks = [[int(elem.text.split(' ')[-1][1:]) for elem in tik_data[0].find_all('a')]]

    tik_data.pop(-4)
    tik_data.pop(0)

    for line in tik_data:
        tik_data_uiks.append([int(c.text.split('\n')[0]) for c in line.find_all('td')])

    tik_number = options_tag.text.split(' ')[0]

    for j in range(len(tik_data_uiks[0])):
        row = [tik_number]
        for k in range(15):
            row.append(tik_data_uiks[k][j])

        row[0] = "ТИК №" + str(row[0])
        row[1] = "УИК №" + str(row[1])
        columns.append(row)


with open('data/elections.csv', "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(columns)
