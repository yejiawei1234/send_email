import os
import re


class Affiliate:

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.android_dir = None
        self.ios_dir = None
        self.root = None
        self.email_attachment = {}
        self.find_dir()
        self.find_affiliate_name()

    def find_dir(self):
        _dirlist = os.listdir('reportgenerator-7')
        self.root = os.path.abspath('reportgenerator-7')
        dirlist = []
        for dirname in _dirlist:
            if dirname.startswith('.'):
                pass
            else:
                dirlist.append(int(dirname))
        target_dir = str(max(dirlist))
        abs_target_dir = os.path.join(self.root, target_dir)
        _sub_0 = 'live.me'
        _sub_android = 'com.cmcm.live'
        _sub_ios = 'id1089836344'

        self.android_dir = os.path.join(abs_target_dir, _sub_0, _sub_android)
        self.ios_dir = os.path.join(abs_target_dir, _sub_0, _sub_ios)

    def find_affiliate_name(self):
        _android = {}
        _ios = {}
        pattern = re.compile(r'((?<=@).*)((?<=@).*\.csv)')
        for i in os.listdir(self.android_dir):
            match = pattern.search(i)
            affiliate_name = match.group(2).split(".")[0]
            _android[affiliate_name] = i
        if self.name in _android.keys():
            attachment_path = os.path.join(self.root, self.android_dir, _android[self.name])
            self.email_attachment['android'] = attachment_path
        for i in os.listdir(self.ios_dir):
            match = pattern.search(i)
            affiliate_name = match.group(2).split(".")[0]
            _ios[affiliate_name] = i
        if self.name in _ios.keys():
            attachment_path = os.path.join(self.root, self.ios_dir, _ios[self.name])
            self.email_attachment['ios'] = attachment_path
