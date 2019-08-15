import os, shutil, time, pickle, threading
import DriveUpload, VideoEditor, YouTubeUpload, LinkShortner

from pathlib import Path

UPLOAD_TYPE_PDF = 100
UPLOAD_TYPE_VIDEO = 102

videosDirectory = os.getcwd() + "/videos"
defaultVideoExtension = ".mp4"

BOOKS = []
UPLOADS = {}
DriveUploadQueue = []
EditQueue = []
YouTubeUploadQueue = []


class Book:

    def __init__(self, directory):
        self.directory = directory
        self.relDirectory = directory.relative_to(os.getcwd())
        self.bookName = directory.relative_to(os.getcwd() + "/Books/pending/")
        self.bookName = str(os.path.splitext(self.bookName)[0])
        self.relDirectory = str(self.relDirectory)

        self.driveUrl = None
        self.shortUrl = None

        self.videoPath = os.path.join(videosDirectory, self.bookName + defaultVideoExtension)

        self.video_edited = False

        if(os.path.exists(self.videoPath)):
            self.video_edited = True

        self.isComplete = False

    def get_pdf_path(self):
        return self.relDirectory

    def get_drive_url(self):
        return self.driveUrl

    def set_drive_url(self, url):
        self.driveUrl = url

    def get_short_url(self):
        return self.shortUrl

    def set_short_url(self, url):
        self.shortUrl = url

    def is_video_edited(self):
        return self.video_edited

    def set_video_edited(self):
        self.video_edited = True

    def get_video_location(self):
        return self.videoPath

    def is_completed(self):
        return self.isComplete

    def set_completed(self):
        self.isComplete = True

    def get_book_name(self):
        return self.bookName

    def get_title(self):
        return self.bookName + " Free Download"

    def get_description(self):
        return "Download:\n" + \
               self.shortUrl + \
               "\n\nDisclaimer:\n" + \
               "All the books uploaded on this channel is done through an automated process and we do not own any content posted here." \
               "\n If you want any of the video to be deleted please contact us at the email below. Thank You." + \
               "\n\nREQUEST A BOOK:\nitsbooks4you@gmail.com"


def dump():
    with open('books.pkl', 'wb') as f:
        pickle.dump(BOOKS, f)
    print("Dumped pickle")

def dump_uploads():
    with open('uploads.pkl', 'wb') as f:
        pickle.dump(UPLOADS, f)
    print("Dumped pickle")


def start_editing():
    if len(EditQueue) != 0:
        for book in EditQueue:
            if not book.is_video_edited():
                VideoEditor.generateVideo(book.get_pdf_path(), book.get_book_name())
                book.set_video_edited()
                YouTubeUploadQueue.append(book)
                dump()


def start_uploading():
    indexb = 0
    while True:
        if len(YouTubeUploadQueue) != 0:
            for book in YouTubeUploadQueue:
                if book.is_completed():
                    print(book.get_book_name() + " is already completed.")
                    continue
                if book.get_drive_url() == None:
                    break
                if book.get_short_url() == None:
                    book.set_short_url(LinkShortner.getShortUrl(book.get_drive_url()))
                print(book.get_book_name() + " is already uploaded to google drive.")

                id, done = YouTubeUpload.upload_video(path=book.videoPath, title=book.get_title(),
                                              description=book.get_description())
                if done:
                    book.set_completed()
                    UPLOADS[book.get_book_name()] = [book.get_drive_url(), book.get_short_url(), id]
                    dump_uploads()
                    shutil.move(book.get_pdf_path(), "Books/completed/" + book.get_book_name() + ".pdf")
                    dump()

        if len(DriveUploadQueue) != 0 and len(DriveUploadQueue) > indexb:
            book = DriveUploadQueue[indexb]
            indexb += 1
            book.set_drive_url(DriveUpload.uploadFile(book.get_pdf_path(), book.bookName))
            book.set_short_url(LinkShortner.getShortUrl(book.get_drive_url()))
            dump()

        print("Uploader Running")
        time.sleep(10)


def startWork():
    for book in BOOKS:
        if not book.is_completed():
            if book.get_drive_url() == None:
                DriveUploadQueue.append(book)
            elif book.get_short_url() == None:
                book.set_short_url(LinkShortner.getShortUrl(book.get_drive_url()))
            else:
                print("Books %s already uploaded to gDrive" % book.get_book_name())
            if not book.is_video_edited():
                EditQueue.append(book)
            elif not book.is_completed():
                print("Books %s video already edited" % book.get_book_name())
                YouTubeUploadQueue.append(book)

    t1 = threading.Thread(target=start_uploading)
    t2 = threading.Thread(target=start_editing)

    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()


def main():
    global BOOKS, UPLOADS
    if os.path.exists(os.getcwd() + '\\books.pkl') and os.path.getsize(os.getcwd() + '\\books.pkl') > 0:
        with open('books.pkl', 'rb') as f:
            f.seek(0)
            BOOKS = pickle.load(f)
        startWork()

    if os.path.exists(os.getcwd() + '\\uploads.pkl') and os.path.getsize(os.getcwd() + '\\uploads.pkl') > 0:
        with open('uploads.pkl', 'rb') as f:
            f.seek(0)
            UPLOADS = pickle.load(f)

    files = Path(str(os.getcwd()) + "/Books/pending/").glob('**/*.pdf')
    for file in files:
        print(file.relative_to(os.getcwd()))
        BOOKS.append(Book(file))

    dump()

    startWork()


if __name__ == '__main__':
    main()
