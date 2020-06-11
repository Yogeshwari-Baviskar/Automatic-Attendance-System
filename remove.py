import os
import shutil

def removeFile(id,course_id):
    path='dataSet/' + str(course_id) + '/' + str(id)
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        return -1

    shutil.rmtree(path, ignore_errors=True)
    return 1

def removeDir(course_id):
    path = 'dataSet/' + str(course_id)
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        return -1

    shutil.rmtree(path, ignore_errors=True)
    return 1
