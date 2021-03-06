import base64
import collections
import operator
import os

import time

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

PACKAGES_SAVE_PATH = "./packages_save/"


class PackageManager:
    def __init__(self, licenses=None, name=None, md5=None):
        self.name = name
        self.license = licenses
        self.md5 = md5

    def get_package_info(self):
        xml_path = PACKAGES_SAVE_PATH + self.license + "/" + self.md5 + "/package.xml"
        xml_root = ET.ElementTree(file=xml_path).getroot()

        return {
            "name": xml_root.find('name').text,
            "author": xml_root.find('author').text,
            "type": xml_root.find('type').text,
            "version": xml_root.find('version').text,
            "createtime": xml_root.find('createtime').text,
            "md5": self.md5,
            "application": xml_root.find('application').text,
        }

    def get_versions(self):
        package_list = os.listdir(PACKAGES_SAVE_PATH + self.license)

        # find latest version at date
        version_index = []
        for file in package_list:
            file_path = "%s%s/%s/package.xml" % (PACKAGES_SAVE_PATH, self.license, file)
            # print("walking xml: " + file_path)

            # xml resolution
            try:
                xml_root = ET.ElementTree(file=file_path).getroot()
            except NotADirectoryError:
                continue

            # get create time
            create_time = xml_root.find('createtime').text
            create_time = time.mktime(time.strptime(create_time, '%Y-%m-%d %H:%M:%S'))

            # sort new > old
            try:
                # print(version_index)
                # print(versions[-1][0])
                if create_time < version_index[-1][0]:
                    # print("s " + str(create_time))
                    version_index.append((create_time, file))
                else:
                    # print("b " + str(create_time))
                    version_index.insert(-1, (create_time, file, "b"))
            except IndexError:
                # print("n " + str(create_time))
                version_index.append((create_time, file))

        # insert version info
        versions = []
        for value in version_index:
            pi = PackageManager(licenses=self.license, md5=value[1]).get_package_info()
            versions.append(pi)

        print(versions)
        return versions

    @staticmethod
    def get_list():
        # Get package library list
        package_list = os.listdir(PACKAGES_SAVE_PATH)
        for i in range(len(package_list)):
            # Get license info
            debase64 = base64.b64decode(package_list[i]).decode()
            license_info = debase64.split(":")
            # Get latest package info

            info = {
                "name": license_info[0],
                "author": license_info[1],
                "license": package_list[i],
                "updatadate": "",
                "latest": ""
            }

            package_list[i] = info

        return package_list


if __name__ == '__main__':
    PackageManager("VGVzdFBhY2thZ2U6SGF0ZWZ1bF9DYXJyZTE6QXpBT3dOeE5CdG11").get_versions()
