from todoapp import app


def main():
    app.run(host='172.18.102.104', port=80, debug=True)

if __name__ == '__main__':
    main()
