import psycopg2
from random import randint
from watson_developer_cloud import ToneAnalyzerV3, NaturalLanguageClassifierV1, NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as \
    features


class DataManager():
    def __init__(self, understanding_username, understanding_password, analyzer_username, analyzer_password,
                 postgresql_username, postgresql_password, postgresql_host, postgresql_dbname):


        self.tone_analyzer = ToneAnalyzerV3(version='2016-02-11', username=analyzer_username,
                                            password=analyzer_password)

        self.natural_language_understanding = NaturalLanguageUnderstandingV1(version='2017-02-27',
                                                                             username=understanding_username,
                                                                             password=understanding_password)

        self.conn_string = "host='{}' dbname='{}' user='{}' password={}".format(postgresql_host, postgresql_dbname, postgresql_username, postgresql_password)
        self.conn = psycopg2.connect(self.conn_string)
        self.cursor = self.conn.cursor()

    def init(self):
        try:
            self.cursor.execute("SELECT * from PoemLines")
        except:
            print "No Table Exists. Creating one."
            self.cursor.execute(
                "CREATE TABLE PoemLines(ID SERIAL, LINE TEXT ,ANGER INT, DISGUST INT, FEAR INT, JOY INT, SADNESS INT, FILLER BOOLEAN)")

    def reset_cursor(self):
        # conn_string = "host='localhost' dbname='nikole.mcleish@ibm.com' user='nikole.mcleish@ibm.com' password=none"
        self.conn = psycopg2.connect(self.conn_string)
        self.cursor = self.conn.cursor()
        print "Connection to database was reset."

    def get_data(self):
        self.cursor.execute("SELECT * FROM PoemLines ORDER by Id")
        return self.cursor.fetchall()

    def get_item(self, i):
        try:
            update_st = "SELECT * FROM PoemLines WHERE Id=%s"
            self.cursor.execute(update_st, (i,))
            return self.cursor.fetchone()
        except:
            self.reset_cursor()


    def update_item(self, val, i):
        try:
            newtones = self.calc_tones(val) + (i,)
            print newtones
            update_st = "UPDATE PoemLines SET LINE=%s, ANGER=%s, DISGUST=%s, FEAR=%s, JOY=%s, SADNESS=%s, FILLER=%s WHERE Id=%s"
            self.cursor.execute(update_st, newtones)
            self.conn.commit()
        except:
            self.reset_cursor()

    def delete_item(self, i):
        update_st = "DELETE from PoemLines where ID=%s"
        self.cursor.execute(update_st, (i,))
        self.conn.commit()

    def calc_tones(self, line):
        filler = True
        data_store = (line.encode('utf-8'),)
        try:
            response = self.tone_analyzer.tone(text=line)

            for tone in response["document_tone"]["tone_categories"][0]["tones"]:
                if round(tone["score"], 1) >= .3:
                    data_store = data_store + (1,)
                    filler = False
                else:
                    data_store = data_store + (0,)

            if filler:
                data_store = data_store + ('true',)
            else:
                data_store = data_store + ('false',)
            print data_store
            # print(json.dumps(response, indent=2))
            return data_store
        except:
            print "Tone Analyzer Failed"
            return None

    def replace_words(self, feelings, la_poem):
        try:
            la_poem = str(la_poem)
            feelings_nla = \
                self.natural_language_understanding.analyze(text=feelings,
                                                            features=[features.Keywords()])
            poem_nla = \
                self.natural_language_understanding.analyze(text=la_poem,
                                                            features=[features.Keywords()])
            fw = []
            for keyword in feelings_nla["keywords"]:
                fw.append(keyword['text'].encode('utf-8'))
            print fw

            pw = []
            for keyword in poem_nla["keywords"]:
                pw.append(keyword['text'].encode('utf-8'))
            print pw
            x = randint(0, len(pw) - 1)
            y = randint(0, len(fw) - 1)
            return feelings.replace(fw[y], pw[x])
        except:
            print "Natural Language Understanding failed."
            return feelings


    def add_line(self, line):
        try:
            update_st="INSERT INTO PoemLines (LINE, ANGER, DISGUST, FEAR, JOY, SADNESS, FILLER) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            tones = self.calc_tones(line)
            self.cursor.execute(
                update_st,
                tones)
            self.conn.commit()
            return tones
        except:
            self.reset_cursor()

    def create_poem(self, tones, feelings, wr):
        etones = ['ANGER', 'DISGUST', 'FEAR', 'JOY', 'SADNESS']
        selector = "SELECT * FROM PoemLines WHERE"
        needand = False
        for x in range(1, 6):
            if tones[x] == 1:
                if needand == True:
                    selector = selector + " AND"
                selector = selector + " {}=1".format(etones[x - 1])
                needand = True
        print selector
        self.cursor.execute(selector)
        data = self.cursor.fetchall()
        self.cursor.execute("SELECT * FROM PoemLines WHERE FILLER='true'")
        fillers = self.cursor.fetchall()

        poem_str = ""
        try:
            for x in range(0, 5):
                if x % 2 == 0 and randint(0, 10) < 2:
                    line_num = randint(0, len(fillers) - 1)
                    poem_str = poem_str + fillers[line_num][1]
                    fillers.pop(line_num)
                    print 'filler added'
                else:
                    line_num = randint(0, len(data) - 1)
                    poem_str = poem_str + data[line_num][1]
                    data.pop(line_num)
                if not x == 4:
                    poem_str = poem_str + "\n"
            if wr:
                return self.replace_words(poem_str, feelings)
            else:
                return poem_str
        except:
            return ["didnt work"]
