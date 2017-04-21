#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import re
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import User
import hebChatbot
import simplejson
import json
from States import States
import Options_to_classes
# TODO a class for global variables like that
ResetUserChat = "פניה חדשה"
test_checker = True
schedule_checker = True
URL_FOR_TESTS = "http://blich.iscool.co.il/DesktopModules/IS.TimeTable" \
                "/MainHtmlExams.aspx?pid=17&mid=6264&layer=0&cls={}"
SCHEDULE_START = '<input type="hidden" name="dnn$ctr7919$TimeTableView$MainControl$WeekShift" id="dnn_ctr7919_TimeTableView_MainControl_WeekShift" value="0" />'
SCHEDULE_END = "</div></div>"
URL_FOR_SCHEDULE = "http://blich.iscool.co.il/tabid/2117/language/he-IL/Default.aspx"
USERS = {}
USERS_PREV_STATE = {}
CONVERSATION_STUCK = {}

# HTTPRequestHandler class
class MyRequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Analyze parameters
        if self.path.find('?') > -1:
            pathParams = self.path.split("?")[1]
            paramDic = self.CreateParamDic(pathParams)

        client_ip = self.getUrl(paramDic)

        if client_ip not in USERS:
            USERS[client_ip] = User.User(client_ip)
            USERS_PREV_STATE[client_ip] = User.User(client_ip)
            CONVERSATION_STUCK[client_ip] = 0

        # Write content as utf-8 data
        str_first_buttons = '[לוח מבחנים|מערכת שעות]'
        self.wfile.write("שלום ,הגעת לצ'ט בוט של בית ספר בליך נעים להכיר.\r\nבמה אוכל לעזור לך ?\r\n".encode("utf-8"))
        self.wfile.write("תוכל לפנות אליי במלל חופשי ואנסה להבין כיצד לסייע לך :)".encode("utf-8"))
        self.wfile.write(str_first_buttons.encode("utf-8"))

        return

    def return_schedule(self,message,schedule_payload, schedule_con_type):
        option_1 = Options_to_classes.option(1)
        option_2 = Options_to_classes.option(2)
        option_3 = Options_to_classes.option(3)
        array_keys = []
        for key in schedule_payload.items():
            array_keys.append(key[0])
        if message in option_1:
            index = option_1.index(message)-1
            message = array_keys[index]
        elif message in option_2:
            index = option_2.index(message)-1
            message = array_keys[index]
        elif message in option_3:
            index = option_3.index(message)-1
            message = array_keys[index]
        if message in schedule_payload and message in schedule_con_type:
            return (schedule_payload[message], schedule_con_type[message])
        else:
            return (False, False)

    def loop_for_schedule(self,array,nowdays,number):
        for num, hour in enumerate(array):
            if num == 0:
                if number != 0:
                    self.answer += "\r\n" + "ב" + nowdays[number] +" יש לך : "+ "\r\n\r\n"
                else:
                    self.answer += "ב" + nowdays[number] + " יש לך : " + "\r\n\r\n"
                if hour != "":
                    self.answer += "בשעה 0 - " + hour + "\r\n"
            elif hour != "" and num != 0:
                if "     " in hour:
                    array_of_the_hour = hour.split("     ")
                    count = 0
                    for i in array_of_the_hour:
                        if count == 0:
                            self.answer += "בשעה " + str(num) + " : " + i + "\r\n"
                        else:
                            self.answer += "---------->" + i + "\r\n"
                        count += 1
                else:
                    self.answer += "בשעה " + str(num) + " : " + hour + "\r\n"
        self.answer += "\r\n----------------------------------------------------------------------\r\n"

    def find_between(self, s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

    def return_json_file(self, path):
        with open(path, 'rb') as f:
            a = f.read()
        return json.loads(a)

    def return_tests(self, message,tests_urls):
        url = URL_FOR_TESTS.format(tests_urls[message])
        x = urllib.request.urlopen(url)
        x = x.read()
        main_array = []
        try:
            result = re.search('<tr>(.*)</tr>', x.decode('utf-8')).group(1)
            result = result.replace("<td>", "")
            result = result.replace("</td>", "")
            result = result.replace("</tr>", "")
            result = result.replace("<b>", "--")
            result = result.replace("</b>", "--")
            result = result.replace("<tr>", "--")
            result = result.split("--")
            for index in range(0, len(result)):
                if index % 3 == 0:
                    main_array.append(result[index])
                    main_array.append(" : ")
                elif index % 3 == 1:
                    main_array.append(result[index])
                    main_array.append(" - ")
                elif index % 3 == 2:
                    main_array.append(result[index])
                    main_array.append("\r\n")
            return ''.join(main_array)
        except:
            return "אין לך מבחנים תודה לאל !"

    def do_POST(self):
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        # Analyze parameters
        if self.path.find('?') > -1:
            pathParams = self.path.split("?")[1]
            paramDic = self.CreateParamDic(pathParams)
        data = simplejson.loads(self.data_string)
        client_ip = self.getUrl(paramDic)
        message = data['message']
        self.answer = ""

        if USERS_PREV_STATE[client_ip] == USERS[client_ip] and not States.is_edge_state(USERS[client_ip].CURRENT_STATE):
            CONVERSATION_STUCK[client_ip] += 1
        else:
            CONVERSATION_STUCK[client_ip] = 0
        print("Stuck Times: " + str(CONVERSATION_STUCK[client_ip]))
        print(message)
        if len(message) > 0:
            global test_checker
            global schedule_checker
            user_message = User.UserMessage(USERS[client_ip], message)
            self.answer += hebChatbot.Start(user_message)
            if test_checker is False and schedule_checker is True:
                tests_urls = self.return_json_file('test.json')
                option_1 = Options_to_classes.option(1)
                option_2 = Options_to_classes.option(2)
                option_3 = Options_to_classes.option(3)
                array_keys = []
                for key in tests_urls.items():
                    array_keys.append(key[0])
                if message in tests_urls:
                    self.answer = self.return_tests(message,tests_urls)
                    self.answer += "\r\n" + "אוכל לעזור בעוד משהו ?"
                elif message in option_1:
                    index = option_1.index(message)
                    message = array_keys[index]
                    self.answer = self.return_tests(message, tests_urls)
                    self.answer += "\r\n" + "אוכל לעזור בעוד משהו ?"
                elif message in option_2:
                    index = option_2.index(message)
                    message = array_keys[index]
                    tests = self.return_tests(message, tests_urls)
                    self.answer = tests
                    self.answer += "\r\n" + "אוכל לעזור בעוד משהו ?"
                elif message in option_3:
                    index = option_3.index(message)
                    message = array_keys[index]
                    tests = self.return_tests(message, tests_urls)
                    self.answer = tests
                    self.answer += "\r\n" + "אוכל לעזור בעוד משהו ?"
                else:
                    self.answer = "?"
                    user_message = User.UserMessage(USERS[client_ip], message)
                    self.answer += hebChatbot.Start(user_message)
                test_checker = True
        
            if schedule_checker is False and test_checker is True:
                self.answer = ""
                schedule_payload = self.return_json_file('schedule_payload')
                schedule_con_type = self.return_json_file('schedule_con_type')
                (payload, con_type) = self.return_schedule(message, schedule_payload, schedule_con_type)
                if payload is not False:
                    schedule_checker = True
                    day_1 = []
                    day_2 = []
                    day_3 = []
                    day_4 = []
                    day_5 = []
                    day_6 = []
                    url = URL_FOR_SCHEDULE
                    headers = {'content-type': con_type}
                    response = requests.request("POST", url, data=payload, headers=headers)
                    result = self.find_between(response.text, SCHEDULE_START, SCHEDULE_END)
                    nowdays = re.findall('<td class(.*)', result)[0:6]
                    for num, item in enumerate(nowdays):
                        nowdays[num] = nowdays[num].replace("</td>\r", "")
                        nowdays[num] = nowdays[num].replace("""="CTitle">""", "")
                    a = re.findall('<table width(.*)', result)
                    b = a[0]
                    a.remove(b)
                    for num, item in enumerate(a):
                        item = item.replace("""=\\'100%\\'><tr><td class=\\'TableExamChange\\'>""",
                                            """=\\'100%\\'></table><div class="TTLesson"><b>""")
                        item = item.replace("</td></tr></table>", "</div>")
                        item = item.replace("<br />", " ")
                        item = item[41:]
                        item = item.replace("</b><br>", "--")
                        item = item.replace("""</div><div class="TTLesson"><b>""", "     ")
                        item = item.replace("</b>&nbsp;&nbsp;", "")
                        item = item.replace("<br>", " עם ")
                        item = item[:-7]
                        item = item.replace("בחן", "מבחן")
                        item = item.replace("יטול", "ביטול")
                        print(num, item)
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
                    self.loop_for_schedule(day_1, nowdays, 0)
                    self.loop_for_schedule(day_2, nowdays, 1)
                    self.loop_for_schedule(day_3, nowdays, 2)
                    self.loop_for_schedule(day_4, nowdays, 3)
                    self.loop_for_schedule(day_5, nowdays, 4)
                    self.loop_for_schedule(day_6, nowdays, 5)
                    self.answer += "\r\n" + "אוכל לעזור בעוד משהו ?"
                else:
                    self.answer = "?"
                    user_message = User.UserMessage(USERS[client_ip], message)
                    self.answer += hebChatbot.Start(user_message)
            if "לוח מבחנים" in message:
                self.answer = "איזה כיתה את\ה ?"
                test_checker = False
            elif "מערכת שעות" in message:
                self.answer = "איזה כיתה את\ה ?"
                schedule_checker = False
        else:# No message. Blocked in client side but who knows
            self.answer = "?"
            user_message = User.UserMessage(USERS[client_ip], message)
            self.answer += hebChatbot.Start(user_message)
        if CONVERSATION_STUCK[client_ip] >= 2 and not States.is_edge_state(USERS[client_ip].CURRENT_STATE):
            # Checking third mistake
            if USERS_PREV_STATE[client_ip] == USERS[client_ip]:
                # Reset chat
                message = ResetUserChat
                user_message = User.UserMessage(USERS[client_ip], message)
                answer = "לא הצלחתי להבין אותך, אני ממליץ לפנות טלפונית ל-012 שלוחה 3.\n"
                answer += hebChatbot.Start(user_message)

            CONVERSATION_STUCK[client_ip] = 0

        self.wfile.write(bytes(self.answer, "utf-8"))
        # self.wfile.write(answer.encode("utf-8"))
        USERS_PREV_STATE[client_ip].make_equal(USERS[client_ip])
    def getUrl(self, paramDic):
        client_ip = paramDic["client_ip"]

        # return client_ip
        # TODO For checking two users locall
        port = paramDic["port"]
        return client_ip + ":" + str(port)

    def CreateParamDic(self, path):
        paramsDic = {}

        pathParams = path.split("&")
        for param in pathParams:
            val = param.split("=")
            paramsDic[val[0]] = val[1]

        return paramsDic

    def remove_unwanted_characters(self, message):
        # TODO implement this method so we won't get unwanted characters
        return message

def run():
    print("preparing chatbot...")
    hebChatbot.InitEntities()

    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8082)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print('running server...')
    httpd.serve_forever()

run()