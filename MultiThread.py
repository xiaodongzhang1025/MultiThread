#coding:utf-8
__author__ = 'zhangxiaodong'
import sys
import os
import codecs
import time
import shutil
import codecs
import chardet
import threading

reload(sys)
sys.setdefaultencoding('utf8')
    
def GetDataEncoding(data):
    data_encoding = None
    det_ret = chardet.detect(data)
    if det_ret:
        data_encoding = det_ret['encoding']
        #print det_ret
        #print 'data_encoding', data_encoding
    if data_encoding == 'windows-1251':
        data_encoding = 'gbk'
        #print '    windows-1251 ==> gbk'
    return data_encoding
    
def ThreadProc(para):
    try:
        print threading.current_thread().name, para, 'Enter!!!'
        time.sleep(2)
    except Exception, err:
        #print err
        print '===> Exception'
        print str(err).decode("string_escape")
    finally:
        #pass
        print threading.current_thread().name, 'Exit!!!'
    
def MultiThreadStart(thread_num_max, para_all):
    thread_list = []
    try:
        thread_num = thread_num_max
        if thread_num > len(para_all):
            thread_num = len(para_all)
        for i in range(0, thread_num):
            para_all_len = len(para_all)
            para_len_average = int((para_all_len + thread_num - 1)/thread_num)
            para_len_cure = para_len_average
            if i == thread_num - 1:
                para_len_cure = para_all_len - (i*para_len_average)
            
            para = para_all[(i*para_len_average):(i*para_len_average + para_len_cure)]
            print '\n----------------------------------'
            print '===>', i, para_len_cure, para
            #thread = threading.Thread(target=ThreadProc, name='thread_%d'%i, args = (para, ))
            #thread.daemon = 1
            #thread = threading.Thread(target=ThreadProc, name='thread_%d'%i, args = (para, ), daemon=True)
            thread = threading.Thread(target=ThreadProc, name='thread_%d'%i, kwargs = {'para':para})
            thread_list.append(thread)
            thread.start()
            #thread.join()
    except Exception, err:
        #print err
        print '===> Exception'
        print str(err).decode("string_escape")
    finally:
        return thread_list
    
if "__main__" == __name__:
    print '\n------------------------------The Start-----------------------------'
    start_time = time.clock()
    
    
    #####################################################
    try:
        thread_num_max = 10
        para_all = []
        for i in range(0, 900):
            para_all.append(i)
        
        thread_list = MultiThreadStart(thread_num_max, para_all)
        #for thread in thread_list:
        #    thread.join()
            
        while True:
            active_count = threading.active_count()
            #active_count = len(threading.enumerate())
            if active_count == 1:
                break
    except Exception, err:
        #print err
        print '===> Exception'
        print str(err).decode("string_escape")
    finally:
        #print '===> Finally'
        print ''
    #####################################################
    print '------------------------------The   End-----------------------------'
    end_time = time.clock()
    print 'Time used %s senconds'%(end_time - start_time)
    sys.exit(0)