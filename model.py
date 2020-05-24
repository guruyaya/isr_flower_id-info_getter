from pydal import Field

def define_tables(db):
    db.define_table('flowers',
        Field('name', unique=True),
        Field('is_month_1', 'boolean', default=False),
        Field('is_month_2', 'boolean', default=False),
        Field('is_month_3', 'boolean', default=False),
        Field('is_month_4', 'boolean', default=False),
        Field('is_month_5', 'boolean', default=False),
        Field('is_month_6', 'boolean', default=False),
        Field('is_month_7', 'boolean', default=False),
        Field('is_month_8', 'boolean', default=False),
        Field('is_month_9', 'boolean', default=False),
        Field('is_month_10', 'boolean', default=False),
        Field('is_month_11', 'boolean', default=False),
        Field('is_month_12', 'boolean', default=False),
    )

    db.define_table('images',
        Field('url', unique=True),
        Field('flower_id', db.flowers),
        Field('exif_data', 'text'),
        Field('taken_date'),
    )

    db.define_table('images_predicted',
        Field('image_id', db.images),
        Field('real', db.flowers),
        Field('predicted', db.flowers),
        Field('success', 'boolean'),
        Field('filename')
    )
