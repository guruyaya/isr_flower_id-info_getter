#!/usr/bin/env python
import web
import sys
from pydal import DAL
sys.path.append('.')
from model import define_tables
db = DAL('sqlite://flower_storage.db', folder='./data')

urls = (
    '/', 'flowers',
    '/my-pics/(.*)', 'pics',
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
        <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
        <style>
            img {{ width: 244; height: 244 }}
            li {{ list-style: none; border: solid 1px #006; margin: 5px; width: 244; height: 244; padding: 5px; float: left}}
            h1,h2 {{clear: both}}
        </style>
        <h1><a href="https://he.wikipedia.org/wiki/{title}">{title}</a></h1>
        <p style="clear:both">{next_pages}</p>
        <h2>OK PICS</h2>
        <ul>{ok_pics}</ul>

        <h2>False Positive</h2>
        <ul>{fp_pics}</ul>

        <h2>False Negative</h2>
        <ul>{fn_pics}</ul>

        <p style="clear:both"><a style="clear:both" href="/pics/{next_page}">Next</a></p>
</html>"""
        script = """"""
        next_page_template = '<a style="clear:both" href="/my-pics/{}">{}</a> '
        next_pages = ''.join( [next_page_template.format(a,a) for a in range (flower_id+1, flower_id + 10)] )
        pics = ''
        image_template = '<li data-id={}><img src="/static/{}" /></li>'
        ok_pics_query = db((db.images_predicted.real == flower_id) &
                        (db.images_predicted.predicted == flower_id)).select()
        ok_pics = '';
        for image in ok_pics_query:
            ok_pics += image_template.format(image.id, image.filename)

        fp_pics_query = db((db.images_predicted.real != flower_id) &
                        (db.images_predicted.predicted == flower_id)).select()
        fp_pics = ''
        for image in fp_pics_query:
            fp_pics += image_template.format(image.id, image.filename)

        fn_pics_query = db((db.images_predicted.real == flower_id) &
                        (db.images_predicted.predicted != flower_id)).select()
        fn_pics = ''
        for image in fn_pics_query:
            fn_pics += image_template.format(image.id, image.filename)

        template = template.format(title=db.flowers[flower_id].name, next_pages=next_pages,
                ok_pics=ok_pics, fp_pics=fp_pics, fn_pics=fn_pics,
                next_page=(int(flower_id)+1))
        return template

class del_img:
    def POST(self):
        img_id = web.input(image_id=None)['image_id'];
        if db(db.images.id == img_id).delete():
            db.commit()
            return """{"success": true}"""
        return """{"success": false}"""

if __name__ == "__main__":
    app.run()
