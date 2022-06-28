from flask import Flask


def register_cli(app: Flask):
    @app.cli.command("resetdb")
    def resetdb_command():
        """Here info that will be shown in flask --help"""
        print("resetdb")
        return "demo"
