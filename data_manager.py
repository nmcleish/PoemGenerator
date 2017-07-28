import psycopg2
from random import randint
from watson_developer_cloud import ToneAnalyzerV3, NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as \
    features
import csv


class DataManager():
    def __init__(self, understanding_username, understanding_password, analyzer_username, analyzer_password,
                 postgresql_username, postgresql_password, postgresql_host, postgresql_dbname, postgresql_port):

        self.tone_analyzer = ToneAnalyzerV3(version='2016-02-11', username=analyzer_username,
                                            password=analyzer_password)

        self.natural_language_understanding = NaturalLanguageUnderstandingV1(version='2017-02-27',
                                                                             username=understanding_username,
                                                                             password=understanding_password)

        self.conn_string = "host='{}' dbname='{}' user='{}' password={} port={}".format(postgresql_host,
                                                                                        postgresql_dbname,
                                                                                        postgresql_username,
                                                                                        postgresql_password,
                                                                                        postgresql_port)
        self.conn = psycopg2.connect(self.conn_string)
        self.cursor = self.conn.cursor()

    def init(self):
        try:
            self.cursor.execute("SELECT * FROM PoemLines")
        except:
            self.reset_cursor()
            self.cursor.execute(
                'CREATE TABLE PoemLines(ID SERIAL, LINE TEXT NOT NULL UNIQUE, ANGER BOOLEAN NOT NULL, DISGUST BOOLEAN NOT NULL, FEAR BOOLEAN NOT NULL, JOY BOOLEAN NOT NULL, SADNESS BOOLEAN NOT NULL, FILLER BOOLEAN NOT NULL);')
            self.fill_db("init.csv")
            self.conn.commit()

    def reset_cursor(self):
        self.conn = psycopg2.connect(self.conn_string)
        self.cursor = self.conn.cursor()

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
                    data_store = data_store + ('true',)
                    filler = False
                else:
                    data_store = data_store + ('false',)

            if filler:
                data_store = data_store + ('true',)
            else:
                data_store = data_store + ('false',)
            return data_store
        except:
            return None

    def dom_emotion(self, line):
        data_store = (line.encode('utf-8'),)
        scores = []

        try:
            response = self.tone_analyzer.tone(text=line)

            for tone in response["document_tone"]["tone_categories"][0]["tones"]:
                scores.append(tone["score"])

            max_score = max(scores)
            if max_score == 0:
                return data_store + ('false', 'false', 'false', 'false', 'false', 'true',)
            x = scores.index(max_score)
            for y in range(5):
                if x == y:
                    data_store = data_store + ('true',)
                else:
                    data_store = data_store + ('false',)
            data_store = data_store + ('false',)
            return data_store
        except:
            return None

    def replace_words(self, newpoem, feelings):
        try:
            feelings = str(feelings)
            newpoem = str(newpoem)

            poem_nla = \
                self.natural_language_understanding.analyze(text=newpoem,
                                                            features=[features.Keywords()])
            feelings_nla = \
                self.natural_language_understanding.analyze(text=feelings,
                                                            features=[features.Keywords()])

            fw = []
            for keyword in feelings_nla["keywords"]:
                fw.append(keyword['text'].encode('utf-8'))

            pw = []
            for keyword in poem_nla["keywords"]:
                pw.append(keyword['text'].encode('utf-8'))

            x = randint(0, len(pw) - 1)
            y = randint(0, len(fw) - 1)

            return newpoem.replace(pw[x], fw[y])
        except:
            return None

    def add_line(self, line):
        try:
            update_st = "INSERT INTO PoemLines (LINE, ANGER, DISGUST, FEAR, JOY, SADNESS, FILLER) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            tones = self.calc_tones(line)
            self.cursor.execute(update_st, tones)
            self.conn.commit()
            return tones
        except:
            self.reset_cursor()
            return None

    def create_poem(self, tones, feelings, wr, se, nf):
        etones = ['ANGER', 'DISGUST', 'FEAR', 'JOY', 'SADNESS']
        selector = "SELECT * FROM PoemLines WHERE"
        needand = False
        for x in range(1, 6):
            if tones[x] == 'true':
                if needand == True:
                    if se:
                        selector = selector + " AND"
                    else:
                        selector = selector + " OR"
                selector = selector + " {}='true'".format(etones[x - 1])
                needand = True
        try:
            self.cursor.execute(selector)
            data = self.cursor.fetchall()
            if not nf:
                self.cursor.execute("SELECT * FROM PoemLines WHERE FILLER='true'")
                fillers = self.cursor.fetchall()

            poem_str = ""
        except:
            self.reset_cursor()
            return "Sorry. This feature didn't work."

        try:
            for x in range(0, 5):
                if not nf and x % 2 == 0 and randint(0, 10) < 2:
                    line_num = randint(0, len(fillers) - 1)
                    poem_str = poem_str + fillers[line_num][1]
                    fillers.pop(line_num)
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
            self.reset_cursor()
            return None

    def getlines(self):
        filename = 'save/lines.csv'
        lfile = open(filename, "wb")
        writer = csv.writer(lfile)
        self.cursor.execute("SELECT * FROM PoemLines")
        lines = self.cursor.fetchall()
        for line in lines:
            writer.writerow(line[1:8])
        lfile.close()

    def fill_db(self, filename):
        lineadded = False
        lineskipped = False
        lfile = open(filename, "rb")
        reader = csv.reader(lfile)
        for row in reader:
            try:
                update_st = "INSERT INTO PoemLines (LINE, ANGER, DISGUST, FEAR, JOY, SADNESS, FILLER) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                self.cursor.execute(update_st, row)
                self.conn.commit()
                lineadded = True
            except:
                lineskipped = True
                self.reset_cursor()
        lfile.close()
        flash = 'Import was successful.'
        if lineadded and lineskipped:
            flash = 'Partial Import Successful. Some lines were skipped.'
        if lineskipped and not lineadded:
            flash = 'Import was unsuccessful.'
        return flash

    def clear_db(self):
        try:
            self.cursor.execute('DELETE FROM PoemLines')
            self.conn.commit()
        except:
            self.reset_cursor()
