import os
from app import app
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from ocr import ocr_text
from pdf2image import convert_from_path
from PIL import Image
from demo import main_function
from highlight import highlight_text

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

ALLOWED_EXTEN = set(['pdf'])

@app.route('/')
def upload_form():
    return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_pdf(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTEN


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        flash('No file selected for uploading!')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)
        text = ocr_text(filename)
        t = ' '.join(text.split())
        # print(t)
        links = []
        ans, sent = main_function(t)
        highlight_text(sent, filename)
        plag = 0
        for i in range(len(ans)):
            if ans[i][0] > plag:
                plag = ans[i][0]
            if ans[i][1] not in links:
                links.append(ans[i][1])

        return render_template('upload.html', filename=filename, text=plag, urls=links, copy=text)

    elif file and allowed_pdf(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        images = convert_from_path(file_path)
        temp_images = []
        for i in range(len(images)):
            # images[i].save('sample' + str(i) + '.jpg')
            images[i].save(os.path.join(app.config['UPLOAD_FOLDER'], str(filename) + str(i) + '.jpg'))
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], str(filename) + str(i) + '.jpg')
            temp_images.append(img_path)

        imgs = list(map(Image.open, temp_images))
        min_img_width = min(i.width for i in imgs)

        # find total height of all images
        total_height = 0
        for i, img in enumerate(imgs):
            total_height += imgs[i].height
        # create new image object with width and total height
        merged_image = Image.new(imgs[0].mode, (min_img_width, total_height))
        # paste images together one by one
        y = 0
        for img in imgs:
            merged_image.paste(img, (0, y))
            y += img.height

        merged_image.save(os.path.join(app.config['UPLOAD_FOLDER'], str(filename) + '.jpg'))
        path = str(filename) + '.jpg'
        text = ocr_text(path)
        t = ' '.join(text.split())
        # print(t)
        links = []
        ans, sent = main_function(t)
        highlight_text(sent, path)
        plag = 0
        for i in range(len(ans)):
            if ans[i][0] > plag:
                plag = ans[i][0]
            if ans[i][1] not in links:
                links.append(ans[i][1])

        return render_template('upload.html', filename=path, text=plag, urls=links, copy=text)


    else:
        flash('Allowed image types are -> png, jpg, jpeg, pdf', 'flashes')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


#app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))

if __name__ == "__main__":
    app.run(debug=True, threaded=True,port=8080,use_reloader=False)
