from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class watcher:
    #TODO:retype events methods
    def on_created(event):
        print(f"hey, {event.src_path} has been created!")

    def on_deleted(event):
        print(f"what the f**k! Someone deleted {event.src_path}!")

    def on_modified(event):
        print(f"hey buddy, {event.src_path} has been modified")

    def on_moved(event):
        print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")

    def __init__(self,directory):
        self.directory = directory
        patterns = ["*"]
        ignore_patterns = None
        ignore_directories = False
        case_sensitive = True
        self.my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        self.my_event_handler.on_created = self.on_created
        self.my_event_handler.on_moved = self.on_moved
        self.my_event_handler.on_modified = self.on_modified
        self.my_event_handler.on_deleted = self.on_deleted
        self.go_recursively = True
        self.my_observer = Observer()
        self.my_observer.schedule(self.my_event_handler, self.directory, recursive=self.go_recursively)

    def start(self):
        self.my_observer.start()
    def stop(self):
        self.my_observer.stop()