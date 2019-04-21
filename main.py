import message_db


def main():

    # connect to messages sqlite db
    con, cur = message_db.connect()

    message_db.get_messages(cur, limit=2)

    con.close()
    return


if __name__ == "__main__":
    main()