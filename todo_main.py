from todo import app


def main():
    app.run(host=app.config.get('SERVER_IP'),
            port=app.config.get('SERVER_PORT'),
            debug=app.config.get('DEBUG'))

if __name__ == '__main__':
    main()
