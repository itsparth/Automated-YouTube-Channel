import webbrowser, pyperclip, keyboard
import pyautogui, time, requests, shutil


def getBookCover(bookname, offline = True):
    bookname = bookname.replace(' ', '+')
    url  = "http://bigbooksearch.com/books/" + bookname
    webbrowser.open(url)
    time.sleep(1)
    pyautogui.click(0, 500)

    while True:
        if keyboard.is_pressed('s'):
            pyautogui.click(button='right')
            time.sleep(0.05)
            pyautogui.keyDown('o')
            time.sleep(0.05)
            pyautogui.keyUp('o')
            imagelink = pyperclip.paste()
            response = requests.get(imagelink, stream=True)
            with open('temp/bookcover.png', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            break

        if keyboard.is_pressed('o'):
            break


if __name__ == "__main__":
    getBookCover("Introduction to algorithms 3rd edition")