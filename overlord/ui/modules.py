# -*- coding: utf-8 -*-

from tornado import web


class NavigationBar(web.UIModule):

    def render(self):
        handlers = [
            (r"/", "Dashboard"),
            (r"/resources", "Resource usages"),
            (r"/stats", "Call statistics")
        ]
        return self.render_string("_navigation_bar.html", handlers=handlers)
