from todo import create_app, db, jwt

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        app.run(debug=True, port='5001')
