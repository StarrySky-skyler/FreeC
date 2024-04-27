import os
import shutil
import threading


# 获取系统变量
systemDrive = os.environ.get('systemdrive')
winDir = os.environ.get('windir')
userProfile = os.environ.get('userprofile')
systemDrive += '\\'

# 删除文件字典
filesDict = {
    systemDrive:['.tmp', '._mp', '.log', '.gid',
                 '.chk', '.old'],
    winDir:['.bak']
}
# 删除文件夹字典，只清空，不删除根文件
directoriesDict = {
    systemDrive:['recycled'],
    winDir:['prefetch', 'temp'],
    userProfile:['cookies', 'recent',
                 'Local Settings\\Temporary Internet Files',
                 'Local Settings\\Temp']
}

print_lock = threading.Lock()

def printLock(message):
    """安全输出日志"""
    with print_lock:
        print(message)

def deleteFilesWithExtension(directory, extension):
    """
    递归删除所有指定类型的文件
    param:
    directory: 遍历的文件夹 e.g. D:/demo
    extension: 指定的文件类型 e.g.  .txt
    """
    for root, _, files in os.walk(directory):
        # 遍历文件
        for file in files:
            # 检查文件后缀是否匹配
            if file.endswith(extension):
                filePath = os.path.join(root, file)
                # 删除文件
                try:
                    printLock(f"Deleting: {filePath}")
                    os.remove(filePath)
                    printLock(f"Deleted: {filePath}")
                # 删除文件时异常
                except OSError as e:
                    printLock(f"Error while deleting\n{filePath}\n{e}")

def deleteDirectory(directory):
    """清空文件夹"""
    try:
        printLock(f"Deleting: {directory}")
        shutil.rmtree(directory)
        printLock(f"Deleted: {directory}")
    except Exception as e:
        printLock(f"Error deleting {directory}:\n{e}")

# 线程池
threads = []
diry = 'C:\\Windows\\SoftwareDistribution\\Download\\'
a = threading.Thread(target=deleteDirectory,
                     args=(diry,))
threads.append(a)
# 添加删除文件线程
for path, exts in filesDict.items():
    for ext in exts:
        b = threading.Thread(target=deleteFilesWithExtension, 
                             args=(path, ext))
        threads.append(b)
# 添加删除文件夹线程
for path, directs in directoriesDict.items():
    for direct in directs:
        __path = os.path.join(path, direct)
        c = threading.Thread(target=deleteDirectory,
                             args=(__path,))
        threads.append(c)

if __name__ == '__main__':
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print("Success free C space")
    os.system('pause')
