#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
import User
import hebChatbot
import simplejson
import json
from States import States
import Options_to_classes
# TODO a class for global variables like that
ResetUserChat = "פניה חדשה"
checker = True
URL_FOR_TESTS = "http://blich.iscool.co.il/DesktopModules/IS.TimeTable" \
                "/MainHtmlExams.aspx?pid=17&mid=6264&layer=0&cls={}"
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
            global checker
            user_message = User.UserMessage(USERS[client_ip], message)
            self.answer += hebChatbot.Start(user_message)
            print(checker)
            if checker is False:
                with open('test.json', 'rb') as f:
                    tests_urls = f.read()
                tests_urls = json.loads(tests_urls)
                option_1 = Options_to_classes.option(1)
                option_2 = Options_to_classes.option(2)
                if message in tests_urls:
                    tests = self.return_tests(message, tests_urls)
                    self.answer = tests
                elif message in option_1:
                    index = option_1.index(message)
                    array_keys = []
                    for key in tests_urls.items():
                         array_keys.append(key[0])
                    message = array_keys[index]
                    tests = self.return_tests(message, tests_urls)
                    self.answer = tests
                elif message in option_2:
                    index = option_2.index(message)
                    array_keys = []
                    for key in tests_urls.items():
                        array_keys.append(key[0])
                    message = array_keys[index]
                    tests = self.return_tests(message, tests_urls)
                    self.answer = tests
                checker = True
            if "לוח מבחנים" in message:
                self.answer = "איזה כיתה את\ה ?"
                checker = False
        else:# No message. Blocked in client side but who knows
            self.answer = "?"

        # Check if user is stuck and reset his conversation
        if CONVERSATION_STUCK[client_ip] >= 2 and not States.is_edge_state(USERS[client_ip].CURRENT_STATE):
            # Checking third mistake
            if USERS_PREV_STATE[client_ip] == USERS[client_ip]:
                # Reset chat
                message = ResetUserChat
                user_message = User.UserMessage(USERS[client_ip], message)
                self.answer = "לא הצלחתי להבין אותך, אנא פנה לאתר של בליך\n"
                self.answer += hebChatbot.Start(user_message)

            CONVERSATION_STUCK[client_ip] = 0

        self.wfile.write(bytes(self.answer, "utf-8"))
        # self.wfile.write(self.answer.encode("utf-8"))
        USERS_PREV_STATE[client_ip].make_equal(USERS[client_ip])

    def getUrl(self, paramDic):
        client_ip = paramDic["client_ip"]

        # return client_ip
        # TODO For checking two users locally
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