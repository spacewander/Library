# coding: utf-8

from library import db

class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    category = db.Column(db.String(20))
    buydate = db.Column(db.String(20))
    introduction = db.Column(db.Text)

    def __init__(self, title, category="", buydate="", introduction=""):
        # you don`t need to init id
        self.title = title
        self.category = category
        self.buydate = buydate
        self.introduction = introduction

    def __repr__(self):
        if self.id is None :
            return  u'Book: %s Category: %s Buydate: %s' % \
                (self.title, self.category, self.buydate_formula() )

        return u'ID: %i Book: %s Category: %s Buydate: %s' % \
                (self.id, self.title, self.category, self.buydate_formula() )

    __unicode__ = __str__ = __repr__

    def buydate_formula(self):
        return self.buydate.encode('utf-8')

    def reborrow(self):
        pass

