import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
 
 
class ScriptEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)
 
    # 文件移动
    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {src_path} to {dest_path}".format(src_path=event.src_path,
                                                                          dest_path=event.dest_path))
        else:
            print(
                "file moved from {src_path} to {dest_path}".format(src_path=event.src_path, dest_path=event.dest_path))
 
    # 文件新建
    def on_created(self, event):
        if event.is_directory:
            print("directory created:{file_path}".format(file_path=event.src_path))
        else:
            print("file created:{file_path}".format(file_path=event.src_path))
 
    # 文件删除
    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{file_path}".format(file_path=event.src_path))
        else:
            print("file deleted:{file_path}".format(file_path=event.src_path))
 
    # 文件修改
    def on_modified(self, event):
        if event.is_directory:
            print("directory modified:{file_path}".format(file_path=event.src_path))
        else:
            print("file modified:{file_path}".format(file_path=event.src_path))
 
 
if __name__ == "__main__":
    event_handler1 = ScriptEventHandler()
    observer = Observer()
    watch = observer.schedule(event_handler1,
                              path="自己的目录地址",
                              recursive=True)
 
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler2 = LoggingEventHandler()
    observer.add_handler_for_watch(event_handler2, watch)  # 为watch新添加一个event handler
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()