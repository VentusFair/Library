from os import abort
import sqlite3 as sql
from flask import Flask, request, jsonify, make_response
import pdb
import logging

app = Flask(__name__)


def database_connection():
    con = sql.connect("books.db")
    # con.row_factory = sql.Row
    return con


@app.route("/jsonBook", methods=["GET"])
def get_book():
    json_data = request.json
    # # pdb.set_trace()
    # con = database_connection()
    # cur = con.cursor()
    # cur.execute("Select * from Library")
    # con.commit()
    # fetchdata = cur.fetchall()
    # con.close()
    # return jsonify(fetchdata)
    try:
        with sql.connect("books.db") as con:
            cur = con.cursor()
            cur.execute("Select * from Library")
            con.commit()
            fetchdata = cur.fetchall()
            for thing in fetchdata:
                print(thing)
            return jsonify(fetchdata)
    except:
        logging.exception()
        con.rollback()
    finally:
        con.close()
    # return {"data": json_data}


@app.route("/jsonBook/<id>", methods=["DELETE"])
def delete(id):
    pdb.set_trace()
    msg = {"": ""}
    code = 0
    try:
        id_int = int(id)
        con = database_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM Library WHERE Id = ?", (id))
        con.commit()
        con.close()
        code = 204
        msg = {"message": "OK"}
    except:
        msg = {"message": "Not found"}
        code = 404

    finally:
        return make_response(msg, code)


@app.route("/jsonBook", methods=["POST"])
def post_book():
    # pdb.set_trace()
    json_data = request.json
    # print("json_data", json_data)

    try:
        with sql.connect("books.db") as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Library (title, author, pubyear, publisher, desc) VALUES (?, ?, ?, ?, ?)",
                (
                    json_data["title"],
                    json_data["author"],
                    json_data["pubyear"],
                    json_data["publisher"],
                    json_data["desc"],
                ),
            )
            con.commit()
            cur.execute("SELECT ID FROM Library WHERE title = ?", [json_data["title"]])
            id = cur.fetchall()
            print(id)
            return jsonify({"id": id})
    except:
        logging.exception()
        con.rollback()
    finally:
        con.close()


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=9000)
