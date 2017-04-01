# import json
#
# with open('test.json', 'rb') as f:
#     tests_urls = f.read()
# tests_urls = json.loads(tests_urls)
# a = []
# for key in tests_urls.items() :
#     the_key = key[0]
#     if len(the_key) == 3:
#         b = the_key[0] + " "
#         c = the_key[2]
#         d = b+c
#         a.append(d)
#     elif len(the_key) == 4:
#         try:
#             num = int(the_key[2:4])
#             b = the_key[0] + " "
#             c = the_key[2:4]
#             d = b + c
#             a.append(d)
#         except:
#             b = the_key[0:2] + " "
#             c = the_key[3]
#             d = b + c
#             a.append(d)
#     elif len(the_key) == 14:
#         b = the_key[0:2] + " "
#         c = "10 מוזיקה"
#         d = b + c
#         a.append(d)
#     elif len(the_key) == 5:
#         b= the_key[0:2] + " "
#         c= the_key[3:]
#         d = b+c
#         a.append(d)
# print(a)
#
# for i in a:
#     print(i)


# import Options_to_classes
# a = Options_to_classes.option(1)
# b=  Options_to_classes.option(2)
# print(a)
# print(b)
import requests

url = "http://blich.iscool.co.il/tabid/2117/language/he-IL/Default.aspx"

payload = "------WebKitFormBoundaryKWT86OhnbfWfdIuW\r\nContent-Disposition: form-data; name=\"__EVENTTARGET\"\r\n\r\ndnn$ctr7919$TimeTableView$btnChangesTable\r\n------WebKitFormBoundaryKWT86OhnbfWfdIuW\r\nContent-Disposition: form-data; name=\"__EVENTARGUMENT\"\r\n\r\n------WebKitFormBoundaryKWT86OhnbfWfdIuW\r\nContent-Disposition: form-data; name=\"__VIEWSTATE\"\r\n\r\n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\r\n------WebKitFormBoundaryKWT86OhnbfWfdIuW"
headers = {'content-type': "multipart/form-data; boundary=----WebKitFormBoundaryKWT86OhnbfWfdIuW"}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)