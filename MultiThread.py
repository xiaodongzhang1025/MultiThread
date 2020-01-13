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
import multiprocessing

reload(sys)
sys.setdefaultencoding('utf8')
    
def TestThreadProc(para):
    try:
        print threading.current_thread().name, 'Enter!!!'
        time.sleep(2)
    except Exception, err:
        #print err
        print '===> Exception'
        print str(err).decode("string_escape")
    finally:
        #pass
        print threading.current_thread().name, 'Exit!!!'

def TestProcessProc(para):
    try:
        print multiprocessing.current_process().name, 'Enter!!!'
        time.sleep(2)
    except Exception, err:
        #print err
        print '===> Exception'
        print str(err).decode("string_escape")
    finally:
        #pass
        print multiprocessing.current_process().name, 'Exit!!!'
        
def MultiThreadStart(para_all, ThreadProc, thread_num_max = None):
    thread_list = []
    try:
        if thread_num_max == None or thread_num_max < 1:
            thread_num_max = multiprocessing.cpu_count() + 1
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
        
def MultiProcessStart(para_all, ProcessProc, process_num_max = None):
    process_list = []
    try:
        if process_num_max == None or process_num_max < 1:
            process_num_max = multiprocessing.cpu_count()
        process_num = process_num_max
        if process_num > len(para_all):
            process_num = len(para_all)
            
        for i in range(0, process_num):
            para_all_len = len(para_all)
            para_len_average = int((para_all_len + process_num - 1)/process_num)
            para_len_cure = para_len_average
            if i == process_num - 1:
                para_len_cure = para_all_len - (i*para_len_average)
            
            para = para_all[(i*para_len_average):(i*para_len_average + para_len_cure)]
            print '\n----------------------------------'
            print '===>', i, para_len_cure#, para
            process = multiprocessing.Process(target=ProcessProc, name='process_%d'%i, kwargs = {'para':para})
            process_list.append(process)
            process.start()
        
    except Exception, err:
        #print err
        print '===> Exception'
        print str(err).decode("string_escape")
    finally:
        return process_list

if "__main__" == __name__:
    print '\n------------------------------The Start-----------------------------'
    start_time = time.clock()
    
    print 'Cpu Count', multiprocessing.cpu_count()
    #####################################################
    try:
        thread_num_max = None
        process_num_max = None
        
        para_all = []
        for i in range(0, 90):
            para_all.append(i)
        
        #thread_list = MultiThreadStart(para_all, TestThreadProc, thread_num_max)
        task_list = MultiProcessStart(para_all, TestProcessProc, process_num_max)
        
        #print 'active thread count', len(threading.enumerate())#threading.active_count()
        print 'active process count', len(multiprocessing.active_children())
        
        for task in task_list:
            task.join()
            
        #print 'active thread count', len(threading.enumerate()) #threading.active_count()
        print 'active process count', len(multiprocessing.active_children())
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