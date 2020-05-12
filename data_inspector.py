#!/usr/bin/env python
import web
import sys
from pydal import DAL
sys.path.append('.')
from model import define_tables
db = DAL('sqlite://flower_storage.db', folder='./data')

urls = (
    '/', 'flowers',
    '/pics/(.*)', 'pics',
    '/del_img', 'del_img'
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
        li = u'<li><a href="/pics/{}">{}</a></li>'
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
        </style>
        <h1><a href="https://he.wikipedia.org/wiki/{title}">{title}</a></h1>
        <p style="clear:both">{next_pages}</p>
        <ul>{pics}</ul>
        <p style="clear:both"><a style="clear:both" href="/pics/{next_page}">Next</a></p>
        <script>{script}</script>
</html>"""
        script = """
$('li').dblclick(function() {
    var $this = $(this);
    $this.css({
        'background-color': '#888',
        'opacity': '0.5'
    });
    $.ajax('/del_img',
            {'method': 'post',
            'dataType': 'json',
            data: {
                'image_id': $(this).data('id')
            },
            success: function(data) {
                if (data.success){
                    $this.hide();
                } else {
                    setTimeout(function() {
                        $this.css({
                            'background-color': '#FFF',
                            'opacity': '1'
                        });
                    }, 300);
                }
            },
            error: function() {
                console.log('Fail');
                $this.css({
                    'background-color': '#FFF',
                    'opacity': '1'
                });
            }
    });
})
"""
        next_page_template = '<a style="clear:both" href="/pics/{}">{}</a> '
        next_pages = ''.join( [next_page_template.format(a,a) for a in range (flower_id+1, flower_id + 10)] )
        pics = ''
        image_template = '<li data-id={}><img src="{}" /></li>'
        for image in db(db.images.flower_id == flower_id).select():
            pics += image_template.format(image.id, image.url)

        template = template.format(title=db.flowers[flower_id].name, next_pages=next_pages,
                pics=pics, script=script, next_page=(int(flower_id)+1))
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
