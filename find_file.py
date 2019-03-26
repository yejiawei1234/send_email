import os
import re
from datetime import datetime
from collections import defaultdict
import pprint


class Affiliate:
    _target = 'reportgenerator-7'

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
        _dirlist = os.listdir(self._target)
        self.root = os.path.abspath(self._target)
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


class AffiliateOne(Affiliate):
    _target = 'reportgenerator-1'

    def __init__(self, name, email):
        super().__init__(name, email)
        self.email_attachment = {}
        self.find_dir()
        self.find_affiliate_name()

    def find_dir(self):
        _dirlist = os.listdir(self._target)
        self.root = os.path.abspath(self._target)
        dirlist = []
        for dirname in _dirlist:
            if dirname.startswith('.'):
                pass
            else:
                abs_path = os.path.join(self.root, dirname)
                if self._new_dir(abs_path) == datetime.today().date():
                    dirlist.append(abs_path)
        _sub_0 = 'live.me'
        _sub_android = 'com.cmcm.live'
        _sub_ios = 'id1089836344'
        self.android_dir = [os.path.join(abs_target_dir, _sub_0, _sub_android) for abs_target_dir in dirlist]
        self.ios_dir = [os.path.join(abs_target_dir, _sub_0, _sub_ios) for abs_target_dir in dirlist]

    def _new_dir(self, abspath):
        timestamp = os.path.getmtime(abspath)
        dir_date = datetime.utcfromtimestamp(timestamp).date()
        return dir_date

    def _search_name(self, dir_abspath):

        pattern = re.compile(r'((?<=@).*)((?<=@).*\.csv)')
        for path in os.listdir(dir_abspath):
            match = pattern.search(path)
            affiliate_name = match.group(2).split(".")[0]
            attachment = os.path.join(dir_abspath, path)
            if self.name == affiliate_name:
                self.email_attachment.setdefault(affiliate_name, []).append(attachment)

    def find_affiliate_name(self):
        for i in self.android_dir:
            self._search_name(i)
        for i in self.ios_dir:
            self._search_name(i)

