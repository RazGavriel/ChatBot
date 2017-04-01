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
import Options_to_classes
a = Options_to_classes.option(1)
b=  Options_to_classes.option(2)
print(a)
print(b)
