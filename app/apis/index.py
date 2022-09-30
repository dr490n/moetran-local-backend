import os
from html import escape
from urllib.parse import unquote, quote

from flask import current_app, redirect, request, send_from_directory, url_for
from app import fileStorage

from app.core.views import MoeAPIView


class IndexAPI(MoeAPIView):
    def get(self):
        return redirect(url_for("index.docs", path="index.html"))


class DocsAPI(MoeAPIView):
    def get(self, path):
        # Debug模式下,当访问主页时候,自动重新生成文档
        if path.startswith("index.html") and current_app.config.get("DEBUG"):
            os.system("apidoc -i app/ -o docs/")
        return send_from_directory("../docs", path)

class StorageAPI(MoeAPIView):
    def get(self, path):
        name = request.args.get('download', None)
        if name:
            name = name + os.path.splitext(path)[-1]
            resp = send_from_directory(fileStorage.STATIC_PATH, path, as_attachment=True)
            resp.headers["Content-disposition"] = 'attachment; filename=%s' % quote(name)
            return resp
        else:
            return send_from_directory(fileStorage.STATIC_PATH, path)


class PingAPI(MoeAPIView):
    def get(self):
        return "pong"


class UrlListAPI(MoeAPIView):
    def get(self):
        output = "<table>"
        for rule in current_app.url_map.iter_rules():

            options = {}
            for arg in sorted(rule.arguments):
                options[arg] = "<{0}>".format(arg)

            methods = ",".join(rule.methods)
            url = escape(unquote(url_for(rule.endpoint, **options)))
            line = "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                rule.endpoint, methods, url
            )
            output += line
        output += "</table>"
        return output


class ErrorAPI(MoeAPIView):
    def get(self):
        """用于测试异常的报错"""
        int("1.2")  # ValueError: invalid literal for int() with base 10: '1.2'


class WarningAPI(MoeAPIView):
    def get(self):
        """用于测试异常的报错"""
        raise Warning("test warning")
