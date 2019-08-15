from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import fitz


def generatePdfSamples(pdfPath):
    doc = fitz.Document(pdfPath)
    center = int(doc.pageCount / 2)

    page = doc[0]
    pix = page.getPixmap()
    pix.writePNG("temp/bookcover.png")

    pageNames = []
    for i in range(7):
        pageNames.append("temp/page-%s.png" % i)

    doc[8].getPixmap().writePNG(pageNames[0])
    doc[9].getPixmap().writePNG(pageNames[1])
    doc[10].getPixmap().writePNG(pageNames[2])
    doc[center].getPixmap().writePNG(pageNames[3])
    doc[center + 1].getPixmap().writePNG(pageNames[4])
    doc[center + 2].getPixmap().writePNG(pageNames[5])
    doc[doc.pageCount - 10].getPixmap().writePNG(pageNames[6])

    return pageNames


def generateText(bookname):
    '''
    img = Image.new('RGB', (1200, 256), (255, 255, 255))

    font = ImageFont.truetype('arial.ttf', 80)
    d = ImageDraw.Draw(img)
    d.text((10, 10), bookname, font=fnt, fill=(0, 0, 0))

    img.save('temp/text.png')
    '''
    import textwrap
    lines = textwrap.wrap(bookname, width=25)
    font = ImageFont.truetype('arial.ttf', 80)
    y_text = 0
    img = Image.new('RGB', (1200, 256), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    w=1000
    for line in lines:
        width, height = font.getsize(line)
        draw.text((10, y_text), line, font=font, fill=(0, 0, 0))
        y_text += height

    img.save('temp/text.png')


def get_pdf_pages_as_array(pdfnames, fwidth, fheight, time=4, count=7):
    height = (ImageClip("temp/page-0.png")
              .resize(width=fwidth)).h

    mul_val = -1 * (abs(height-fheight)/3)
    pdfs = []
    for i, name in enumerate(pdfnames):
        if i > count-1:
            break

        pdf = (ImageClip(name)
                .set_duration(time)
                .resize(width=fwidth)
                .set_pos(lambda t: ('center', fheight/3 + mul_val * t)))
        pdfs.append(pdf)
    return pdfs


def generateVideo(pdfPath, bookname):
    generateText(bookname)

    pdf_names = generatePdfSamples(pdfPath)

    clip = VideoFileClip("editor/samplevideo.mp4")

    bookcover = (ImageClip("temp/bookcover.png")
                 .set_duration(5.8)
                 .resize(height=600)  # if you need to resize...
                 .margin(left=100, top=100, opacity=0)  # (optional) logo-border padding
                 .set_pos(("left", "top")))

    title = (ImageClip("temp/text.png")
             .set_duration(5.8)  # if you need to resize...
             .margin(right=100, opacity=0)  # (optional) logo-border padding
             .set_pos(("right", "center")))

    pdfs = get_pdf_pages_as_array(pdf_names, clip.w, clip.h, time=4, count=7)

    startTime = 14.5
    delay = 4
    compArray = [clip, bookcover.set_start(8).crossfadein(1).crossfadeout(1),
                                title.set_start(8).crossfadein(1).crossfadeout(1)]

    for i, pdf in enumerate(pdfs):
        compArray.append(pdf.set_start(startTime + i*delay).crossfadein(1).crossfadeout(1))

    final = CompositeVideoClip(compArray)
    final.write_videofile("videos/" + bookname + ".mp4", threads=4, progress_bar=False, fps=30)

    return "videos/" + bookname + ".mp4"


if __name__ == '__main__':
    generateText("Hello this is parth rathore and you are watching coldfusion tv")