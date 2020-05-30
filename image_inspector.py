#!/usr/bin/env python
import web
import sys, os, re, shutil
import json
from pydal import DAL
sys.path.append('.')
from model import define_tables
db = DAL('sqlite://flower_storage.db', folder='./data')

urls = (
    '/', 'flowers',
    '/my-pics/(.*)', 'pics',
    '/update_image', 'update_image'
)
app = web.application(urls, globals())

define_tables(db)

class flowers:
    def GET(self):
        template = u"""<html>
        <meta charset="UTF-8">
        <ul>{flower_list}</ul>
</html>"""
        flower_list = ''
        li = u'<li><a href="/my-pics/{}">{}</a></li>'
        for flower in db().select(db.flowers.ALL):
            flower_list += li.format(flower.id, flower.name)

        template = template.format(flower_list=flower_list)
        return template

class pics:
    def GET(self, flower_id):
        flower_id = int(flower_id)
        template = u"""<html>
        <title>{title}</title>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css" />
        <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
        <script
			  src="https://code.jquery.com/ui/1.12.0/jquery-ui.min.js"
			  integrity="sha256-eGE6blurk5sHj+rmkfsGYeKyZx3M4bG+ZlFyA7Kns7E="
			  crossorigin="anonymous"></script>
<link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-beta.1/dist/css/select2.min.css" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-beta.1/dist/js/select2.min.js"></script>
        <style>
            img {{ width: 244; height: 244 }}
            ul.img_list li {{ list-style: none; border: solid 1px #006; margin: 5px; width: 244; height: 244; padding: 5px; float: left}}
            h1,h2,h3 {{clear: both}}
            form {{display: none}}
            #show_images {{position: fixed; width: 100%; border: solid 1px #777; bottom: 3px; background-color: white; display: none; height: 350px}}
        </style>
        <h1><a href="https://he.wikipedia.org/wiki/{title}">{title}</a></h1>
        <p style="clear:both">{next_pages}</p>
        <h2>OK PICS</h2>
        <ul class="img_list">{ok_pics}</ul>

        <h2>Wrongly Unassigned (Should be {title})</h2>
        <ul class="img_list">{fn_pics}</ul>

        <h2>Wrongly Assigned (Not really {title})</h2>
        <ul class="img_list">{fp_pics}</ul>

        <p style="clear:both"><a style="clear:both" href="/my-pics/{next_page}">Next</a></p>

        <form id="set_flower_real_cat">
            <input type="hidden" id="image_id" name="image_id">
            <h3>Predicted <span id="predicted_text"></span>, Real <span id="real_text"></span></h3>
            <img id="flower_image" /><br />
            <select id="flower_id" name="flower_id">
            </select>
            <input type="button" value="Submit" id="flower_data_submit" />
            <ul id="target_images" class="img_list">
            </ul>
        </form>
        <div id="show_images">
            <h3><span id="show_images_name"></span> Images</h3>
            <ul id="show_images_target_images" class="img_list">
            </ul>
        </div>
        <script>{all_flowers}</script>
        <script>{script}</script>
</html>"""
        script = """
const show_form = function () {
    const set_form_real_images = function() {
        let target_images = $('#target_images').html('');
        let this_flower_id = $('#flower_id').val();
        if (this_flower_id != 'delete') {
            let flower_data = all_flowers[this_flower_id];
            for (let i=0; i<flower_data.images.length;i++) {
                let li = $('<li></li>');
                let img = $('<img />').attr('src', '/static/' + flower_data.images[i])
                li.append(img);
                target_images.append(li);
            }
        }
    }
    const submit_update = function () {
        $('#flower_data_submit').attr('disabled', true);
        $.ajax({
            'url': '/update_image',
            'method': 'post',
            'dataType': 'json',
            'data': $('form#set_flower_real_cat').serialize(),
            'success': function(data) {
                $('#flower_data_submit').attr('disabled', false);
                if (data.success){
                    $('form#set_flower_real_cat').dialog('close')
                    window.location.reload()
                }else{
                    alert('ERR1')
                }
            },
            'error': function () {
                $('#flower_data_submit').attr('disabled', false);
            }
        });
    }
    const flower_id_select = $('#flower_id');
    $('#flower_data_submit').attr('disabled', false).on('mousedown', submit_update);
    $('#image_id').val($(this).data('id'))
    $('#predicted_text').html($(this).data('predicted'));
    $('#real_text').html($(this).data('real'));
    flower_id_select.html('');

    for (var i in all_flowers){
        let flower_data = all_flowers[i];
        let option = $('<option></option>').attr({
            value: flower_data.flower[0]
        }).html(flower_data.flower[1]);

        if (flower_data.flower[0] == $(this).data('prefered_id')){
            option.attr('selected', true)
            flower_id_select.prepend(option)
        }else{
            flower_id_select.append(option)
        }
    }
    flower_id_select.prepend($('<option></option>').attr('value', 'delete').html('DELETE?!!'))
    flower_id_select.on('change', set_form_real_images);
    $('#flower_image').attr('src', $(this).find('img').attr('src'));
    set_form_real_images();
    $('form#set_flower_real_cat').dialog({'width': '80%'})
    $('select').select2()


}
$('h3.show_images').on('mouseover', function() {
    let this_flower_id = $(this).data('flower_id');
    let flower_data = all_flowers[this_flower_id];
    let target_images = $('#show_images_target_images').html('');

    $('#show_images_name').html(flower_data.flower[1])
    for (let i=0; i<flower_data.images.length;i++) {
        let li = $('<li></li>');
        let img = $('<img />').attr('src', '/static/' + flower_data.images[i])
        li.append(img);
        target_images.append(li);
    }

    $('#show_images').show();
}).on('mouseout', function() {
    $('#show_images').hide();
});
$('li').on('click', show_form);
"""

        flower_name = db.flowers[flower_id].name
        all_flowers_query = db().select(db.images_predicted.ALL, db.flowers.ALL,
                    left=db.flowers.on(db.images_predicted.real == db.flowers.id))

        all_flowers_list = {}
        i = 0
        for f_img in all_flowers_query:
            if f_img.flowers.id not in all_flowers_list.keys():
                all_flowers_list[ f_img.flowers.id ] = {
                    'flower': (f_img.flowers.id, f_img.flowers.name),
                    'images': []
                }
            if (len( all_flowers_list[ f_img.flowers.id ]['images']) < 3 ):
                all_flowers_list[ f_img.flowers.id ]['images'] += [f_img.images_predicted.filename]
        all_flowers = "const all_flowers = " + json.dumps(all_flowers_list)
        next_page_template = '<a style="clear:both" href="/my-pics/{}">{}</a> '
        next_pages = ''.join( [next_page_template.format(a,a) for a in range (flower_id+1, flower_id + 10)] )
        pics = ''
        image_template = '<li data-id={} data-prefered_id={} data-predicted="{}" data-real="{}"><img src="/static/{}" /></li>'

        ok_pics_query = db((db.images_predicted.real == flower_id) &
                        (db.images_predicted.predicted == flower_id)).select()
        ok_pics = '';
        for image in ok_pics_query:
            ok_pics += image_template.format(image.image_id, image.real, flower_name, flower_name, image.filename)

        fp_pics_query = db((db.images_predicted.real != flower_id) &
                        (db.images_predicted.predicted == flower_id)).select()
        fp_pics_arranged = fp_pics_query.group_by_value(db.images_predicted.real)

        fp_pics = ''
        for wrong_flower_id, images in fp_pics_arranged.items():
            flower = db.flowers[ wrong_flower_id ]
            fp_pics += '<h3 class="show_images" data-flower_id="{}"><a href="/my-pics/{}">{}</h3></a>'.format(flower.id, flower.id, flower.name)
            for image in images:
                fp_pics += image_template.format(image.image_id, image.predicted, flower_name, flower.name, image.filename)

        fn_pics_query = db((db.images_predicted.real == flower_id) &
                        (db.images_predicted.predicted != flower_id)).select()
        fn_pics_arranged = fn_pics_query.group_by_value(db.images_predicted.predicted)

        fn_pics = ''
        for wrong_flower_id, images in fn_pics_arranged.items():
            flower = db.flowers[ wrong_flower_id ]
            fn_pics += '<h3 class="show_images" data-flower_id="{}"><a href="/my-pics/{}">{}</h3></a>'.format(flower.id, flower.id, flower.name)
            for image in images:
                fn_pics += image_template.format(image.image_id, image.predicted, flower.name, flower_name, image.filename)

        template = template.format(title=db.flowers[flower_id].name, next_pages=next_pages,
                ok_pics=ok_pics, fp_pics=fp_pics, fn_pics=fn_pics, script=script,
                next_page=(int(flower_id)+1), all_flowers=all_flowers)
        return template

class update_image:
    def delete_image(self, image_id):
        # get filename
        image_predicted = db.images_predicted(image_id=image_id)
        filename = image_predicted.filename
        # remove from filesystem
        try:
            os.remove ('data/images/{}'.format(filename))
        except FileNotFoundError:
            pass
        # remove from images_predicted
        db(db.images_predicted.image_id == image_id).delete()
        # remove from images
        db(db.images.id == image_id).delete()
        db.commit()
        return """{"success": true}"""
    def update_image_flower_id(self, image_id, flower_id):
        # get_filename
        image_predicted = db.images_predicted(image_id=image_id)
        filename = image_predicted.filename
        # set target filename
        target = re.sub('^[0-9]*/', '{}/'.format(flower_id), filename)
        # move file
        try:
            shutil.move( 'data/images/{}'.format(filename), 'data/images/{}'.format(target))
        except FileNotFoundError:
            pass
        # update images_predicted
        db(db.images_predicted.image_id == image_id).update(filename=target, real=flower_id)
        # update image
        db(db.images.id==image_id).update(flower_id=flower_id)
        db.commit()
        return """{"success": true}"""

    def POST(self):
        web.header('Content-Type', 'application/json')
        image_id = web.input(image_id=None)['image_id'];
        flower_id = web.input(flower_id=None)['flower_id'];
        if flower_id == 'delete':
            return self.delete_image(image_id)
        else:
            return self.update_image_flower_id(image_id, flower_id)
        return """{"success": false}"""

if __name__ == "__main__":
    app.run()
