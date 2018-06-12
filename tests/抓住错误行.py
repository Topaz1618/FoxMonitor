#_*_coding:utf-8_*_
# Author:Topaz
import sys
try:
        a = [1,2]
        print(a[3])
except:
        s = sys.exc_info()
        print("Error '%s' happened on line %d" % (s[1],s[2].tb_lineno))