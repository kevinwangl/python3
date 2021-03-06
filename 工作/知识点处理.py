import pymysql
import random


def get_db():
    # 打开数据库连接
    try:
        # db = pymysql.connect(
        #     host="123.206.227.74", user="root",
        #     password="exue2017", db="zujuan_spark_test", port=3306,
        #     charset="utf8"
        # )
        db = pymysql.connect(
            host="localhost", user="root",
            password="kuaikang", db="kuaik", port=3333,
            charset="utf8"
        )
        return db
    except Exception as e:
        print(e)


def insert_tag():
    db = get_db()
    cur = db.cursor()
    cur.execute("select tag_description from t_res_dl_tag")
    result = cur.fetchall()
    s = set()
    for res in result:
        tags = res[0].split(";")
        for tag in tags:
            s.add(tag.replace("\n", "").strip())
    sql_insert_tag = "INSERT INTO t_res_dl_tag_copy (`tag_id`, `tag_name`) " \
                     "VALUES ('{tag_id}', '{tag_name}');"
    tag_id = 21000000
    for i in s:
        cur.execute(sql_insert_tag.format(tag_id=tag_id, tag_name=i))
        tag_id += 1
        db.commit()
    cur.close()
    db.close()


def main():
    db = get_db()
    cur = db.cursor()
    sql = "select tag_id,question_uuid from t_res_dl_tag_question"
    select_tag_by_id = "select tag_description from t_res_dl_tag where tag_id = %s"
    select_tag_by_name = "select tag_id from t_res_dl_tag_copy where tag_name = '%s'"
    insert_tag_question = "INSERT INTO t_res_dl_tag_question_copy (`tag_id`, `tag_name`, `question_uuid`, `create_time`) " \
                          "VALUES ('{tag_id}', '{tag_name}', '{question_uuid}', '2018-03-20 21:02:48');"
    cur.execute(sql)
    tag_question_map = cur.fetchall()
    for m in tag_question_map:
        cur.execute(select_tag_by_id % m[0])
        tag_name = cur.fetchone()
        tag_list = tag_name[0].replace("\n", "").split(";")
        for t in tag_list:
            cur.execute(select_tag_by_name % t)
            tag_id = cur.fetchone()[0]
            cur.execute(insert_tag_question.format(tag_id=tag_id, tag_name=t, question_uuid=m[1]))
        db.commit()
    cur.close()
    db.close()


if __name__ == '__main__':
    main()
