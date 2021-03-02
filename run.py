from app import create_app


app = create_app("dev")


# if __name__ == "__main__":
#     app.jinja_env.cache = {}
#     app.jinja_env.auto_reload = True
#     app.run(debug=True)
