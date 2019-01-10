from pymysql import connect


class JD():
    def __init__(self):
        # 1.创建connection连接
        self.conn = connect(host='localhost',port=3306,user='root',password='123456',database='jing_dong',charset='utf8')
        # 2.获得cursor对象
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    @staticmethod
    def print_menu():
        print("---------商城菜单--------")
        print("1:所有的商品")
        print("2:所有的商品分类")
        print("3:所有的商品品牌分类")
        print("0:退出")
        return input("请输入功能相对应的序号：")

    def show_all_items(self):
        sql = "select * from goods;"
        self.cursor.execute(sql)
        print("+"*50)
        for temp in self.cursor.fetchall():
            print(temp)
        print("+"*51)

    def show_cates(self):
        sql = "select name from goods_cates;"
        self.cursor.execute(sql)
        print("+"*50)
        for temp in self.cursor.fetchall():
            print(temp)
        print("+"*50)

    def show_brand(self):
        sql = "select name from goods_brands;"
        self.cursor.execute(sql)
        print("+"*50)
        for temp in self.cursor.fetchall():
            print(temp)
        print("+"*50)

    def run(self):
        while True:
            op = self.print_menu()

            if op == "1":
                # 查询所有商品
                self.show_all_items()
            elif op == "2":
                # 查询所有商品的分类
                self.show_cates()
            elif op == "3":
                # 查询所有品牌的分类：
                self.show_brand()
            elif op == "0":
                break
            else:
                print("您的输入有误，请重新输入。。。。。")


def main():
    # 1.创建一个实例对象
    jd = JD()
    # 2.调用实例方法
    jd.run()


if __name__ == "__main__":
    main()
