#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
-------------------------------------------------
@File    : result_analysis.py
@Time    : 2021/1/15 7:02 下午
@Author  : Han0nly
@Github  : https://github.com/Han0nly
@Email   : zhangxh@stu.xidian.edu.cn
-------------------------------------------------
"""

import pymongo, json
import logging
import config
import openpyxl


class MobSF_result:
    def __init__(self, colname=None):
        """
        MobSF_result object constructor.
        """
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.dbip = config.dbip
        self.dbport = config.dbport
        if colname:
            self.colname = colname
        else:
            self.colname = config.colname
        self.dbname = config.dbname
        self._connect()

    ##############################
    # Internal Methods #
    ##############################

    def _connect(self):
        client = pymongo.MongoClient(f'mongodb://{self.dbip}:{self.dbport}')
        db = client[self.dbname]
        self.conn = db[self.colname]
        self._getcontents()

    def _getcontents(self):
        self.content = []
        self.count = 0
        for item in self.conn.find():
            self.count = self.count + 1
            self.content.append(item['result'])

    ##############################
    # External Methods #
    ##############################

    def write_contents2file(self, file_name: str = 'mobsf_result.json'):
        with open(file_name, 'w+') as f:
            f.write(json.dumps(self.content, ensure_ascii=False, indent=2))

    def get_notification(self):
        self.apps_detail = {}
        use_notification_platform = []
        for item in self.content:
            for mani in item['manifest_analysis']:
                if "title" in mani.keys() and "description" in mani.keys():
                    if "Notification Platform" == mani["description"]:
                        use_notification_platform.append(mani["title"])
            for api in item["android_api"]:
                if "Jiguang_sdk" in api.keys():
                    use_notification_platform.append("Jiguang")
                if "pusher_sdk" in api.keys():
                    use_notification_platform.append("Pusher")
                if "kumulos_sdk" in api.keys():
                    use_notification_platform.append("kumulos")
                if "airship_sdk" in api.keys():
                    use_notification_platform.append("airship")
                if "onesignal_sdk" in api.keys():
                    use_notification_platform.append("onesignal")
                if "taplytics_sdk" in api.keys():
                    use_notification_platform.append("taplytics")
                if "leanplum_sdk" in api.keys():
                    use_notification_platform.append("leanplum")
                if "IBM_sdk" in api.keys():
                    use_notification_platform.append("IBM")
                if "pushbot_sdk" in api.keys():
                    use_notification_platform.append("pushbot")
                if "iGexin_sdk" in api.keys():
                    use_notification_platform.append("iGexin")
            self.apps_detail[item['file_name']] = set(use_notification_platform)


if __name__ == '__main__':
    result = MobSF_result("GooglePlay")
    result.get_notification()
    count = 0
    statistics = {"Jiguang": 0, "Pusher": 0, "kumulos": 0, "airship": 0, "onesignal": 0, "IBM": 0, "taplytics": 0,
                  "leanplum": 0, "pushbot": 0, "iGexin": 0}
    for i in result.apps_detail.keys():
        if len(result.apps_detail[i]) > 0:
            count = count + 1
            for key in statistics.keys():
                if key in result.apps_detail[i]:
                    statistics[key] = statistics[key] + 1
    print("\nTotal: %d\n" % len(result.apps_detail.keys()))
    print(
        "Use Notification Platform: {}, accounting for {:.2f}\n".format(count, count / len(result.apps_detail.keys())))
    for key in result.apps_detail.keys():
        print(
            "{}: {}, accounting for {:.2f}\n".format(key, statistics[key], statistics[key] / len(result.apps_detail.keys())))
