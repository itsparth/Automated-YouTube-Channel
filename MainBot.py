import os, shutil, multiprocessing
from pathlib import Path
import DriveUpload, VideoEditor, YouTubeUpload, LinkShortner

pendingPDF = "/Books/pending/"
donePDF = "/Books/completed/"


def doWorkForOne(path):
    bookpath = str(path)
    bookwithext = bookpath.split('\\')[-1]
    bookname = bookwithext.split('.')[0]
    bookpath = "Books/pending/" + bookwithext
    print(bookpath)
    bookUrl = DriveUpload.uploadFile(filepath=bookpath, filename=bookname)

    videopath = VideoEditor.generateVideo(pdfPath=bookpath, bookname=bookname)

    title = bookname + " Free Ebook Download"
    description = "DOWNLOAD:\n" + LinkShortner.getShortUrl(bookUrl) + "\n\n"
    description = description + "DISCLAIMER:\nAll the books uploaded on this channel is done through an automated process and we do not own any content posted here.\n If you want any of the video to be deleted please contact us at the email below. Thank You."
    description = description + "\n\nREQUEST A BOOK:\nitsbooks4you@gmail.com"
    YouTubeUpload.upload_video(filename=videopath, title=title, description=description)

    print("Moving book to completed")
    shutil.move(bookpath, "Books/completed/" + bookwithext)
    print("Done")
    return


def main():

    destdir = os.fsencode(os.getcwd() + pendingPDF)
    files = Path(destdir)

    for file in files:
        doWorkForOne(file)
    return

if __name__ == '__main__':
    main()
