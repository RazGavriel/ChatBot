import urllib.request
import json
import re
import requests
with open('schedule_payload', 'rb') as f:
    schedule_payload = f.read()
schedule_payload = json.loads(schedule_payload)

with open('schedule_con_type', 'rb') as f:
    schedule_con_type = f.read()
schedule_con_type = json.loads(schedule_con_type)
array_keys = []
for count, item in enumerate(schedule_payload):
     array_keys.append(item)

def find_between(s, first, last):
     try:
         start = s.index(first) + len(first)
         end = s.index(last, start)
         return s[start:end]
     except ValueError:
         return ""
url = "http://blich.iscool.co.il/tabid/2117/language/he-IL/Default.aspx"
payload = schedule_payload[array_keys[27]]
headers = {'content-type': schedule_con_type[array_keys[27]]}
response = requests.request("POST", url, data=payload, headers=headers)
result = find_between(response.text, '<input type="hidden" name="dnn$ctr7919$TimeTableView$MainControl$WeekShift" id="dnn_ctr7919_TimeTableView_MainControl_WeekShift" value="0" />', "</div></div>")
nowdays= re.findall('<td class(.*)',result)
nowdays = nowdays[0:6]
for num ,item in enumerate(nowdays):
    nowdays[num] = nowdays[num].replace("</td>\r", "")
    nowdays[num] = nowdays[num].replace("""="CTitle">""", "")
a = re.findall('<table width(.*)', result)
b = a[0]
a.remove(b)
day_1 =[]
day_2 =[]
day_3 =[]
day_4 =[]
day_5 =[]
day_6 =[]
for num,item in enumerate(a):
    item = item [41:]
    item = item.replace("</b><br>", "--")
    item = item.replace("""</div><div class="TTLesson"><b>""", ",")
    item = item.replace("</b>&nbsp;&nbsp;", "")
    item = item.replace("<br>", "")
    item = item[:-7]
    if num % 6 == 0:
        day_1.append(item)
    elif num % 6 == 1:
        day_2.append(item)
    elif num % 6 == 2:
        day_3.append(item)
    elif num % 6 == 3:
        day_4.append(item)
    elif num % 6 == 4:
        day_5.append(item)
    elif num % 6 == 5:
        day_6.append(item)
print(day_1)

        # try:
#     result = re.search('<tr>(.*)</tr>', x.decode('utf-8')).group(1)
#     result = result.replace("<td>", "")
#     result = result.replace("</td>", "")
#     result = result.replace("</tr>", "")
#     result = result.replace("<b>", "--")
#     result = result.replace("</b>", "--")
#     result = result.replace("<tr>", "--")
#     result = result.split("--")
#     for index in range(0, len(result)):
#         if index % 3 == 0:
#             main_array.append(result[index])
#             main_array.append(" : ")
#         elif index % 3 == 1:
#             main_array.append(result[index])
#             main_array.append(" - ")
#         elif index % 3 == 2:
#             main_array.append(result[index])
#             main_array.append("\r\n")
#     return ''.join(main_array)
# except:
#     return "אין לך מבחנים תודה לאל !"


