import urllib.request
import urllib.parse
import re
import json
URL_FOR_TESTS = "http://blich.iscool.co.il/DesktopModules/IS.TimeTable" \
                "/MainHtmlExams.aspx?pid=17&mid=6264&layer=0&cls={}"
HELLO_SENTENCE = "שלום הגעת לצ'ט בוט של בליך איך אני יכול לעזור ?"

def main():
    print(HELLO_SENTENCE)

    with open('test.json', 'rb') as f:
        tests_urls = f.read()

    tests_urls = json.loads(tests_urls)
    massage = input("איזה כיתה את/ה ?")

    while massage not in tests_urls:
        massage = input("איזה כיתה את/ה ?")

    url = URL_FOR_TESTS.format(tests_urls[massage])
    x = urllib.request.urlopen(url)
    x = x.read()
    dates = []
    teachers = []
    subject = []
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
            dates.append(result[index])
        elif index % 3 == 1:
            subject.append(result[index])
        elif index % 3 == 2:
            teachers.append(result[index])
    print(teachers)
    print(dates)
    print(subject)
    print(teachers[0] + "\n" + dates[0] + "\n" + subject[0])

if __name__ == '__main__':
    main()
