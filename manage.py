
import datetime
import logging
import tkinter
import tkinter.messagebox
from errno import errorcode
from tkinter import *
from tkinter import messagebox, ttk

from PIL import ImageTk, Image


# 取消按钮的事件处理函数
# 当调用此函数时，会清空str1和str2两个变量的内容
def cancel():
    str1.set('')  # 将str1变量的值设置为空字符串
    str2.set('')  # 将str2变量的值设置为空字符串


# 数据库连接函数
# 该函数用于建立与MySQL数据库的连接
def connect():
    import pymysql  # 导入pymysql库，用于Python连接MySQL数据库
    from pymysql import MySQLError  # 从pymysql库中导入MySQLError，用于处理数据库错误

    try:
        # 尝试使用给定的用户名、密码、主机名和数据库名连接到MySQL数据库
        cnx = pymysql.connect(user='root', password='123456',
                              host='localhost',
                              database='stu')
        print('Connected successfully!')  # 如果连接成功，显示成功消息
        return cnx  # 返回数据库连接对象
    except MySQLError as err:
        # 如果出现MySQL错误，显示错误消息
        print("Failed to connect:", err)



# 添加数据到数据库函数
def addsave(varsno, varsname, varsex, varage, vardept):
    # 使用with语句自动管理数据库连接的创建和关闭
    with connect() as cnx:  # connect()函数返回数据库连接对象
        # 创建游标对象，用于执行SQL语句
        cursor = cnx.cursor()

        try:
            # 构建并执行插入学生信息的SQL语句
            addSQL = "INSERT INTO student (`Sno`,`Sname`,`Ssex`,`Sage`,`Sdept`) VALUES ('%s','%s','%s','%d','%s')" % (
                varsno, varsname, varsex, varage, vardept)
            # 构建并执行插入用户信息的SQL语句，默认密码为"123456"，角色为"user"
            userSQL = "INSERT INTO user_info (`username`,`password`,`role`) VALUES ('%s','%s','%s')" % (
                varsno, "123456", "user")
            # 执行SQL语句，将数据添加到数据库中
            cursor.execute(addSQL)
            cursor.execute(userSQL)

        except Exception as e:
            # 如果执行SQL语句过程中出现异常，回滚事务，保证数据的一致性
            cnx.rollback()
            print("Failed to execute SQL: ", e)

        else:
            # 如果没有异常，提交事务，使数据变更生效
            cnx.commit()
            print("Data saved successfully!")
            # 记录日志，表明数据已成功添加到数据库（假设logger已在外部定义并配置）
            logger.info(f"添加 {varsno} 的信息到数据库")

        finally:
            # 无论是否出现异常，都执行此块代码
            # 打印受SQL语句影响的行数
            print(cursor.rowcount)
            # 关闭游标，释放资源
            cursor.close()


# 添加数据到数据库函数
def addsave(varsno, varsname, varsex, varage, vardept):
    with connect() as cnx:
        # 创建一个数据库游标对象，用于执行SQL查询
        cursor = cnx.cursor()

        try:
            # 构建插入学生信息的SQL语句
            addSQL = "INSERT INTO student (`Sno`,`Sname`,`Ssex`,`Sage`,`Sdept`) VALUES ('%s','%s','%s','%d','%s')" % (
                varsno, varsname, varsex, varage, vardept)
            # 构建插入用户信息的SQL语句，默认密码设置为"123456"，用户角色为"user"
            userSQL = "INSERT INTO user_info (`username`,`password`,`role`) VALUES ('%s','%s','%s')" % (
                varsno, "123456", "user")
            # 执行插入学生信息的SQL语句
            cursor.execute(addSQL)
            # 执行插入用户信息的SQL语句
            cursor.execute(userSQL)

        except Exception as e:
            # 如果在执行SQL语句过程中发生异常，则回滚数据库事务
            # 这可以撤销在事务中所做的任何更改，以保持数据的一致性
            cnx.rollback()
            # 打印异常信息，帮助调试
            print("Failed to execute SQL: ", e)


 # 查询学生信息对应函数
def findsql(varname):
    # 连接数据库
    with connect() as cnx:
        # 创建一个数据库游标对象，用于执行SQL查询和获取结果
        cursor = cnx.cursor()

        try:
            # 构建根据学生姓名查询的SQL语句
            findSQL = "SELECT * FROM student WHERE Sname='%s'" % varname
            # 执行SQL查询
            cursor.execute(findSQL)

            # 获取查询结果的所有行
            rows = cursor.fetchall()
            # 如果没有查询到结果
            if not rows:
                # 弹出一个信息框，提示用户未找到该学生信息
                tkinter.messagebox.showinfo('提示', '未找到该学生信息，请确认输入是否正确')
            else:
                # 遍历查询结果的每一行
                for row in rows:
                    # 打印查询结果
                    print(row)
                    # 初始化水平滚动条和垂直滚动条
                    scrollbar_x = tkinter.Scrollbar(frmd, orient=tkinter.HORIZONTAL)
                    scrollbar_y = tkinter.Scrollbar(frmd, orient=tkinter.VERTICAL)
                    # 创建一个树状视图控件，用于展示查询结果
                    tree = ttk.Treeview(frmd, columns=("Sno", "Name", "Sex", "Age", "Sdept"),
                                        yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
                    # 配置滚动条与树状视图的滚动命令
                    scrollbar_x.config(command=tree.xview)
                    scrollbar_y.config(command=tree.yview)

                    # 设置树状视图的表头
                    tree.heading("#0", text="ID")
                    tree.heading("Sno", text="学号")
                    tree.heading("Name", text="姓名")
                    tree.heading("Sex", text="性别")
                    tree.heading("Age", text="年龄")
                    tree.heading("Sdept", text="专业")

                    # 设置树状视图的列宽
                    tree.column("#0", width=50)
                    tree.column("Sno", width=100)
                    tree.column("Name", width=50)
                    tree.column("Sex", width=50)
                    tree.column("Age", width=50)
                    tree.column("Sdept", width=100)
                    # 禁止第一列的宽度自动调整
                    tree.column("#0", width=0, stretch=tkinter.NO)
                    # 将树状视图放置到指定的网格位置
                    tree.grid(row=3, column=1, sticky=tkinter.NSEW, columnspan=2)

                    # 放置滚动条到指定的网格位置
                    scrollbar_x.grid(row=3, column=1, sticky=tkinter.EW)
                    scrollbar_y.grid(row=3, column=1, sticky=tkinter.NS)
                    # 将查询结果添加到树状视图中
                    tree.insert("", tkinter.END, values=row)

        except Exception as e:
            # 如果在执行SQL查询过程中发生异常，则回滚数据库事务
            cnx.rollback()
            # 打印异常信息
            print("Failed to execute SQL: ", e)

        else:
            # 如果没有异常发生，则提交数据库事务
            cnx.commit()
            # 打印成功找到数据的消息
            print("Data found successfully!")
            # 记录日志，表示已经查询了某个学生的基本信息
            logger.info(f"查询 {varname} 基本信息")

        finally:
            # 无论是否发生异常，都关闭游标对象
            # 连接对象cnx会在with块结束时自动关闭
            cursor.close()



# 查询学生成绩信息的界面和函数
def findgrade(sno):
    print("查询学生成绩信息")
    for widget in frmd.winfo_children():
        widget.grid_forget()
    # 创建表格组件
    scrollbar_x = tkinter.Scrollbar(frmd, orient=tkinter.HORIZONTAL)
    scrollbar_y = tkinter.Scrollbar(frmd, orient=tkinter.VERTICAL)
    tree = ttk.Treeview(frmd, columns=("Cno", "Cname", "Grade"), yscrollcommand=scrollbar_y.set,
                        xscrollcommand=scrollbar_x.set)
    scrollbar_x.config(command=tree.xview)
    scrollbar_y.config(command=tree.yview)

    tree.heading("#0", text="ID")
    tree.heading("Cno", text="课程号")
    tree.heading("Cname", text="课程名")
    tree.heading("Grade", text="成绩")

    tree.column("#0", width=70)
    tree.column("Cno", width=70)
    tree.column("Cname", width=150)
    tree.column("Grade", width=70)
    tree.column("#0", width=0, stretch=tkinter.NO)
    tree.grid(row=1, sticky=tkinter.NSEW, columnspan=3)

    scrollbar_x.grid(row=1, column=1, sticky=tkinter.EW)
    scrollbar_y.grid(row=1, column=1, sticky=tkinter.NS)
    # 连接数据库
    with connect() as cnx:
        # 创建游标对象
        cursor = cnx.cursor()

        try:

            findSQL = "SELECT sc.Cno,course.Cname,sc.Grade " \
                      "FROM sc JOIN course ON sc.Cno=course.Cno WHERE sc.Sno=%s"
            # 执行 SQL 语句
            cursor.execute(findSQL, (sno,))

            # 获取所有结果行
            rows = cursor.fetchall()

            # 清空表格
            tree.delete(*tree.get_children())

            # 将查询结果添加到表格中
            for row in rows:
                tree.insert("", tkinter.END, values=row)

        except Exception as e:
            # 发生异常时，回滚事务
            cnx.rollback()
            print("Failed to execute SQL: ", e)

        else:
            # 提交事务
            cnx.commit()
            print("Data found successfully!")

        finally:
            # 关闭游标和连接对象
            cursor.close()

# 将管理员录入的成绩写入数据库
def gradesave(newgrade):
    with connect() as cnx:
        # 创建一个游标对象，用于执行SQL语句
        cursor = cnx.cursor()

        try:
            # 遍历传入的成绩数据
            for row in newgrade:
                # 定义更新成绩的SQL语句模板
                updateSQL = "UPDATE sc SET Grade=%s WHERE Sno=%s AND Cno=%s"
                # 其中row[2]是成绩，row[0]是学生编号，row[1]是课程编号
                cursor.execute(updateSQL, (row[2], row[0], row[1]))

        except Exception as e:
            # 如果执行SQL语句过程中出现异常，回滚事务，以保持数据的一致性
            cnx.rollback()
            # 打印异常信息
            print("Failed to execute SQL: ", e)

        else:
            # 如果没有异常，提交事务，确保数据被保存到数据库中
            cnx.commit()
            # 打印成功信息
            print("grade update successfully!")
            logger.info(f"录入选修 {row[1]} 号课程的同学成绩信息")

        finally:
            # 关闭游标和连接对象
            cursor.close()


# 查找选修某门课程的学生信息对应的函数——用于管理员根据课程信息修改学生成绩
def findcno(Cno):
    # 创建一个新的Frame框架，用于在界面上展示查询结果
    frme = Frame(frmd)
    frme.grid(row=3, columnspan=3)
    # 清除框架上已有的所有组件，以便重新添加新的组件
    for widget in frme.winfo_children():
        widget.grid_forget()

        # 连接数据库
    with connect() as cnx:
        # 创建游标对象，用于执行SQL查询
        cursor = cnx.cursor()
        try:
            # 定义并执行参数化的SQL查询语句，查找选修了指定课程的学生信息和成绩
            findSQL = "SELECT student.sno, student.Sname, sc.grade " \
                      "FROM sc INNER JOIN student ON sc.Sno = student.Sno " \
                      "WHERE sc.Cno = %(Cno)s"
            cursor.execute(findSQL, {'Cno': Cno})

            # 初始化一个空列表，用于存储更新后的成绩信息
            newgrade = []
            # 初始化行号，用于在界面上定位组件的位置
            i = 4

            # 定义一个内部函数，用于创建展示学生信息和成绩的界面组件
            def create(i):
                # 创建并定位学号标签
                labelsno = tkinter.Label(frme, text=row[0], width=20)
                labelsno.grid(row=i, column=1, padx=5, pady=10)
                # 创建并定位姓名标签
                labelsname = tkinter.Label(frme, text=row[1], width=20)
                labelsname.grid(row=i, column=2, pady=10, padx=5)
                # 创建一个StringVar对象，用于与成绩输入框绑定
                vargrade = tkinter.StringVar()
                vargrade.set(row[2])
                # 创建并定位成绩输入框
                entryGrade = tkinter.Entry(frme, textvariable=vargrade, width=20)
                entryGrade.grid(row=i, column=3, pady=10, padx=5)
                # 将学号、课程号和当前成绩作为一个元组添加到newgrade列表中
                newgrade.append((row[0], Cno, vargrade.get()))

                # 定义一个内部函数，用于监视成绩输入框内容的变化，并更新newgrade列表中的对应成绩
                def update_newgrade(*args):
                    for j in range(len(newgrade)):
                        if newgrade[j][0] == row[0]:
                            newgrade[j] = (row[0], Cno, vargrade.get())
                            break


                 # 为成绩输入框添加一个写入追踪，当成绩发生变化时，调用update_newgrade函数
                vargrade.trace_add('write', update_newgrade)

                # 获取查询结果中的所有行

            rows = cursor.fetchall()
            # 创建并定位表头标签（学号、姓名、成绩）
            label1 = tkinter.Label(frme, text="学号", width=20)
            label1.grid(row=3, column=1, padx=5, pady=10)
            label2 = tkinter.Label(frme, text="姓名", width=20)
            label2.grid(row=3, column=2, padx=5, pady=10)
            label3 = tkinter.Label(frme, text="成绩", width=20)
            label3.grid(row=3, column=3, pady=10, padx=5)

            # 遍历查询结果，为每个学生创建展示信息的组件
            for row in rows:
                print(row)  # 打印查询结果，用于调试
                create(i)  # 调用create函数，为学生创建界面组件
                i = i + 1  # 更新行号，以便下一个学生的组件能够正确定位

            # 创建一个保存按钮，点击时调用gradesave函数，将更新后的成绩保存到数据库中
            buttonsave = tkinter.Button(frme, text="commit", command=lambda: gradesave(newgrade))
            buttonsave.grid(row=i, columnspan=3, padx=20, pady=10)

        except Exception as e:
            # 如果在执行SQL查询过程中发生异常，回滚事务并打印错误信息
            cnx.rollback()
            print("Failed to execute SQL: ", e)

        else:
            # 如果没有发生异常，提交事务并打印成功信息
            cnx.commit()
            print("Data found successfully!")

        finally:
            # 无论是否发生异常，都关闭游标和数据库连接
            cursor.close()


# 定义一个函数，名为deletesql，用于删除指定学生的信息
def deletesql(sname):
    # 首先调用findsql函数，查询或确认学生的信息
    findsql(sname)

    # 弹出一个消息框，询问用户是否确定要删除此学生
    result = messagebox.askyesno("确认", "你确定要删除此学生吗？")

    # 如果用户点击确定
    if result:
        # 使用上下文管理器（with语句）来连接数据库，确保资源被正确管理
        with connect() as cnx:
            # 创建一个游标对象，用于执行SQL语句
            cursor = cnx.cursor()

            try:
                # 执行SQL语句，从sc表中删除指定学生的所有成绩记录
                delscSQL = "DELETE FROM sc WHERE Sno IN (SELECT Sno FROM student WHERE Sname='%s')" % sname
                cursor.execute(delscSQL)

                # 执行SQL语句，从student表中删除指定学生的记录
                delstSQL = "DELETE FROM student WHERE Sname='%s'" % sname
                cursor.execute(delstSQL)

            except Exception as e:
                # 如果在执行SQL语句过程中出现异常，回滚事务，确保数据的完整性
                cnx.rollback()
                print("执行SQL失败：", e)

            else:
                # 如果没有异常，提交事务，使更改生效
                cnx.commit()
                print("Data delete successfully!")
                # 记录日志，表明已成功删除指定学生的信息（注意：logger需要用户自行定义和配置）
                logger.info(f"删除 {sname} 的信息")

            finally:
                # 无论是否发生异常，都关闭游标和数据库连接，释放资源
                cursor.close()


    else:
        print("取消")


# 定义一个函数，名为upsql，用于更新学生信息
def upsql(oldname, sname, sex, age, dept):
    # 检查新姓名是否为空，如果为空则抛出ValueError异常
    if not sname:
        raise ValueError("新姓名不能为空")

        # 检查年龄是否在1到10000岁之间，如果不在则抛出ValueError异常
    if age < 1 or age > 10000:
        raise ValueError("年龄必须在1到10000岁之间")

    with connect() as cnx:
        # 创建一个游标对象，用于执行SQL语句
        cursor = cnx.cursor()

        # 构造SQL语句，检查新姓名是否已存在于student表中
        check_name_sql = "SELECT COUNT(*) FROM student WHERE Sname = %s"
        cursor.execute(check_name_sql, (sname,))
        # 执行SQL语句并获取结果
        result = cursor.fetchone()
        # 如果结果中计数大于0，说明新姓名已存在，抛出ValueError异常
        if result[0] > 0:
            raise ValueError("新姓名已存在，请选择其他姓名")

        try:
            # 构造SQL语句，用于更新student表中的学生信息
            updateSQL = "UPDATE student SET Sname=%s, Ssex=%s, Sage=%s, Sdept=%s WHERE Sname=%s"
            # 执行SQL更新语句
            cursor.execute(updateSQL, (sname, sex, age, dept, oldname))

            # 提交事务，使更改生效
            cnx.commit()
            print("数据更新成功！")
            # 记录日志，表明已成功修改指定学生的基本信息（注意：logger需要用户自行定义和配置）
            logger.info(f"修改 {oldname} 的基本信息")

        except Exception as e:
            # 如果在执行SQL语句过程中出现异常，回滚事务，确保数据的完整性
            cnx.rollback()
            print("执行 SQL 失败：", e)

        finally:
            # 无论是否发生异常，都关闭游标，释放资源
            cursor.close()


# 创建和显示修改学生基本信息的界面函数
def updatesql(sname):
    def handle_selection():
        print(varSex.get())

    row = findsql(sname)
    for rows in row:
        # 与姓名相关的变量
        varName = tkinter.StringVar()
        varName.set(rows[1])
        # 创建标签，并放在frmd上
        labelName = tkinter.Label(frmd, text='学生姓名', width=10)
        labelName.grid(row=3, column=1)
        # 创建文本框，同时设置关联的变量
        entryName = tkinter.Entry(frmd, width=14, textvariable=varName)
        entryName.grid(row=3, column=2, pady=10, padx=5)
        # 设置学生性别单选框
        labelSex = tkinter.Label(frmd, width=6, text='性别')
        labelSex.grid(row=4, column=1, padx=3, pady=10)
        labelSex.config(anchor=tkinter.E)
        varSex = tkinter.StringVar()
        varSex.set(rows[2])  # 默认性别为男
        radioSex1 = tkinter.Radiobutton(frmd, text='男', variable=varSex, width=8, value='男', command=handle_selection)
        radioSex1.grid(row=4, column=2, padx=5, pady=10)
        radioSex2 = tkinter.Radiobutton(frmd, text='女', variable=varSex, width=8, value='女', command=handle_selection)
        radioSex2.grid(row=4, column=3, pady=10, padx=5)
        # 设置学号输入框
        varSno = tkinter.StringVar()
        varSno.set(rows[0])
        labelSno = tkinter.Label(frmd, width=6, text='学号')
        labelSno.grid(row=5, column=1, pady=10, padx=5)
        entrySno = tkinter.Entry(frmd, width=14, textvariable=varSno)
        entrySno.grid(row=5, column=2, padx=5, pady=10)
        # 设置年龄输入框
        varAge = tkinter.IntVar(value=rows[3])
        labelAge = tkinter.Label(frmd, width=6, text='年龄')
        labelAge.grid(row=6, column=1, pady=10, padx=5)
        entryAge = tkinter.Entry(frmd, width=14, textvariable=varAge)
        entryAge.grid(row=6, column=2, padx=5, pady=10)
        # 设置专业下拉项
        labelDept = tkinter.Label(frmd, width=6, text='专业')
        labelDept.grid(row=7, column=1, padx=10, pady=5)
        varDept = tkinter.StringVar()
        spinValues = ('Gloves', 'TaiKnife', 'TwinGuns','HeavyArtillery')
        varDept.set(rows[4])
        spinValues = (varDept.get(),) + spinValues
        spinDept = tkinter.Spinbox(frmd, textvariable=varDept, values=spinValues, wrap=True)
        spinDept.grid(row=7, column=2, padx=10, pady=5)
        # 创建保存按钮
        buttonSave = tkinter.Button(frmd, text="保存",
                                    command=lambda: upsql(rows[1], varName.get(), varSex.get(), varAge.get(),
                                                          varDept.get()))
        buttonSave.grid(row=8, column=2, padx=10, pady=5)


# sort()函数
def sortsql(Cno):
    with connect() as cnx:
        # 创建游标对象
        cursor = cnx.cursor()

        try:
            # 构建SQL查询语句，根据课程号(Cno)查询学生姓名、学号和成绩，并按成绩降序排序
            sortSQL = 'SELECT student.sname,sc.Sno, sc.Grade "' \
                      '"FROM sc INNER JOIN student ON sc.Sno = student.Sno WHERE ' \
                      'sc.Cno = %s ORDER BY sc.Grade DESC' % Cno

            #执行SQL语句
            cursor.execute(sortSQL)

            # 获取所有结果行
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            scrollbar_x = tkinter.Scrollbar(frmd, orient=tkinter.HORIZONTAL)
            scrollbar_y = tkinter.Scrollbar(frmd, orient=tkinter.VERTICAL)
            tree = ttk.Treeview(frmd, columns=("Name", "Sno", "Grade"),
                                yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
            scrollbar_x.config(command=tree.xview)
            scrollbar_y.config(command=tree.yview)

            tree.heading("#0", text="ID")
            tree.heading("Name", text="姓名")
            tree.heading("Sno", text="学号")
            tree.heading("Grade", text="成绩")

            tree.column("#0", width=50)
            tree.column("Name", width=50)
            tree.column("Sno", width=100)
            tree.column("Grade", width=50)
            tree.column("#0", width=0, stretch=tkinter.NO)
            tree.grid(row=3, column=1, sticky=tkinter.NSEW, columnspan=2)

            frmd.grid_rowconfigure(3, weight=1)
            frmd.grid_columnconfigure(1, weight=1)

            tree.grid(row=3, column=1, sticky="nsew", columnspan=2)

            scrollbar_x.config(command=tree.xview)
            scrollbar_y.config(command=tree.yview)
            for row in rows:
                tree.insert("", tkinter.END, values=row)

            # 重新计算表格尺寸
            tree.update()
        except Exception as e:
            # 发生异常时，回滚事务
            cnx.rollback()
            print("Failed to execute SQL: ", e)

        else:
            # 提交事务
            cnx.commit()
            print("Data sort successfully!")
            logger.info(f"依据 {Cno} 的成绩排序")

        finally:
            # 关闭游标和连接对象
            cursor.close()


# 添加学生信息对应函数 - 界面
def add():
    print("调用了add()函数")
    # 移除frmd框架的所有组件
    for widget in frmd.winfo_children():
        widget.grid_forget()

    def handle_selection():
        print(varSex.get())

    # 与姓名相关的变量
    varName = tkinter.StringVar()
    varName.set('')
    # 创建标签，并放在frmd上
    labelName = tkinter.Label(frmd, text='学生姓名', width=10)
    labelName.grid(row=1, column=1)
    # 创建文本框，同时设置关联的变量
    entryName = tkinter.Entry(frmd, width=14, textvariable=varName)
    entryName.grid(row=1, column=2, pady=10, padx=5)
    # 设置学生性别单选框
    labelSex = tkinter.Label(frmd, width=6, text='性别')
    labelSex.grid(row=2, column=1, padx=3, pady=10)
    labelSex.config(anchor=tkinter.E)
    varSex = tkinter.StringVar()
    varSex.set('女')  # 默认性别为男
    radioSex1 = tkinter.Radiobutton(frmd, text='男', variable=varSex, width=8, value='男', command=handle_selection)
    radioSex1.grid(row=2, column=2, padx=5, pady=10)
    radioSex2 = tkinter.Radiobutton(frmd, text='女', variable=varSex, width=8, value='女', command=handle_selection)
    radioSex2.grid(row=2, column=3, pady=10, padx=5)
    # 设置学号输入框
    varSno = tkinter.StringVar()
    labelSno = tkinter.Label(frmd, width=6, text='学号')
    labelSno.grid(row=3, column=1, pady=10, padx=5)
    entrySno = tkinter.Entry(frmd, width=14, textvariable=varSno)
    entrySno.grid(row=3, column=2, padx=5, pady=10)
    # 设置年龄输入框
    varAge = tkinter.IntVar(value='')
    labelAge = tkinter.Label(frmd, width=6, text='年龄')
    labelAge.grid(row=4, column=1, pady=10, padx=5)
    entryAge = tkinter.Entry(frmd, width=14, textvariable=varAge)
    entryAge.grid(row=4, column=2, padx=5, pady=10)
    # 设置专业下拉项
    labelDept = tkinter.Label(frmd, width=6, text='专业')
    labelDept.grid(row=5, column=1, padx=10, pady=5)
    varDept = tkinter.StringVar()
    spinDept = tkinter.Spinbox(frmd, textvariable=varDept, values=('Gloves', 'TaiKnife', 'TwinGuns','HeavyArtillery'), wrap=True)
    spinDept.grid(row=5, column=2, padx=10, pady=5)

    # 创建保存按钮
    buttonSave = tkinter.Button(frmd, text="保存",
                                command=lambda: addsave(varSno.get(), varName.get(), varSex.get(), varAge.get(),
                                                        varDept.get()))
    buttonSave.grid(row=6, column=2, padx=10, pady=5)


# 添加学生信息对应函数 - 界面
def add():
    print("调用了add()函数")
    # 移除frmd框架的所有组件
    for widget in frmd.winfo_children():
        widget.grid_forget()

        # 创建学生信息输入框和标签
    labelName = tkinter.Label(frmd, text='学生姓名', width=10)
    labelName.grid(row=1, column=1, pady=5, padx=5)
    varName = tkinter.StringVar()
    entryName = tkinter.Entry(frmd, width=20, textvariable=varName)
    entryName.grid(row=1, column=2, pady=5, padx=5)

    labelSex = tkinter.Label(frmd, text='性别', width=6)
    labelSex.grid(row=2, column=1, pady=5, padx=5)
    varSex = tkinter.StringVar()
    radioSex1 = tkinter.Radiobutton(frmd, text='男', variable=varSex, value='男')
    radioSex1.grid(row=2, column=2, pady=5, padx=5)
    radioSex2 = tkinter.Radiobutton(frmd, text='女', variable=varSex, value='女')
    radioSex2.grid(row=2, column=3, pady=5, padx=5)

    labelSno = tkinter.Label(frmd, text='学号', width=6)
    labelSno = tkinter.Label(frmd, text='学号', width=6)
    labelSno.grid(row=3, column=1, pady=5, padx=5)
    varSno = tkinter.StringVar()
    entrySno = tkinter.Entry(frmd, width=20, textvariable=varSno)
    entrySno.grid(row=3, column=2, pady=5, padx=5)

    labelAge = tkinter.Label(frmd, text='年龄', width=6)
    labelAge.grid(row=4, column=1, pady=5, padx=5)
    varAge = tkinter.IntVar()
    entryAge = tkinter.Entry(frmd, width=20, textvariable=varAge)
    entryAge.grid(row=4, column=2, pady=5, padx=5)

    labelDept = tkinter.Label(frmd, text='专业', width=6)
    labelDept.grid(row=5, column=1, pady=5, padx=5)
    varDept = tkinter.StringVar()
    entryDept = tkinter.Entry(frmd, width=20, textvariable=varDept)
    entryDept.grid(row=5, column=2, pady=5, padx=5)

    # 创建保存按钮
    buttonSave = tkinter.Button(frmd, text="保存",
                                command=lambda: add_student(varName.get(), varSex.get(), varSno.get(), varAge.get(),
                                                            varDept.get()))
    buttonSave.grid(row=6, column=2, padx=10, pady=5)


def add_student(sname, ssex, sno, sage, sdept):
    try:
        # 调用addsave函数将学生信息添加到数据库
        addsave(sno, sname, ssex, int(sage), sdept)
        tkinter.messagebox.showinfo('添加成功', '学生信息添加成功！')
    except ValueError as e:
        # 如果年龄不是整数，显示错误信息
        tkinter.messagebox.showerror('添加失败', str(e))
    except Exception as e:
        # 其他异常，显示错误信息
        tkinter.messagebox.showerror('添加失败', '添加学生信息时发生错误：' + str(e))

# 查找学生信息对应界面界面
def find():
    print("调用了find()函数")
    # 移除frmd框架的所有组件
    for widget in frmd.winfo_children():
        widget.grid_forget()
    # 按照姓名查找
    # 创建姓名输入框
    namelabel = tkinter.Label(frmd, width=20, text="请输入要查找学生的姓名")
    namelabel.grid(row=1, column=1, pady=5, padx=10)
    varname = tkinter.StringVar()
    nameentry = tkinter.Entry(frmd, width=16, textvariable=varname)
    nameentry.grid(row=1, column=2, pady=5, padx=10)
    # 创建查询按钮
    buttonfind = tkinter.Button(frmd, text="查询", command=lambda: findsql(varname.get()))
    buttonfind.grid(row=2, column=1, padx=100, pady=5, columnspan=2, sticky='nesw')


# 修改学生信息对应界面
def updata():
    print("调用了updata()函数")
    for widget in frmd.winfo_children():
        widget.grid_forget()
    # 创建修改学生信息输入框
    labelsname = tkinter.Label(frmd, text="请输入要修改学生的姓名", width=40)
    labelsname.grid(row=1, column=1, pady=10, padx=5)
    varsname = tkinter.StringVar()
    entrysname = tkinter.Entry(frmd, textvariable=varsname, width=16)
    entrysname.grid(row=1, column=2, padx=5, pady=10)
    # 创建按钮
    buttonupdata = tkinter.Button(frmd, text="查询", command=lambda: updatesql(varsname.get()))  # 先查找，然后在结果上做修改
    buttonupdata.grid(row=2, column=1, padx=100, pady=5, columnspan=2, sticky='nesw')


# 删除学生信息对应界面
def delete():
    print("调用了delete()函数")
    # 移除frmd框架的所有组件
    for widget in frmd.winfo_children():
        widget.grid_forget()
    # 姓名输入框
    labelsname = tkinter.Label(frmd, width=40, text="请输入要删除的学生姓名")
    labelsname.grid(row=1, column=1, padx=5, pady=10)
    varsname = tkinter.StringVar()
    entrysname = tkinter.Entry(frmd, width=16, textvariable=varsname)
    entrysname.grid(row=1, column=2, padx=5, pady=10)
    buttonsname = tkinter.Button(frmd, text="删除", command=lambda: deletesql(varsname.get()))
    buttonsname.grid(row=2, column=1, padx=100, pady=5, columnspan=2, sticky='nesw')


# 学生成绩录入对应的界面
def upgrade():
    print("调用了upgrade()函数")
    for widget in frmd.winfo_children():
        widget.grid_forget()
    # 创建课程号输入框
    labelCno = tkinter.Label(frmd, text="请输入要录入的课程", width=40)
    labelCno.grid(row=1, column=1, padx=5, pady=10)
    varCno = tkinter.StringVar()
    entryCno = tkinter.Entry(frmd, textvariable=varCno, width=16)
    entryCno.grid(row=1, column=2, pady=10, padx=5)
    # 创建查询按钮 - 这里的查询是查询选修了这门课的学生信息
    buttonfind = tkinter.Button(frmd, text="查询", command=lambda: findcno(varCno.get()))
    buttonfind.grid(row=2, column=1, padx=100, pady=5, columnspan=3, sticky='nesw')


# 成绩排序对应界面
def sort():
    print("调用了sort()函数")
    # 移除frmd框架的所有组件
    for widget in frmd.winfo_children():
        widget.grid_forget()
    # 创建课程号输入框
    labelCno = tkinter.Label(frmd, width=40, text="请输入要排序的课程号")
    labelCno.grid(row=1, column=1, pady=10, padx=5)
    varCno = tkinter.StringVar()
    entryCno = tkinter.Entry(frmd, textvariable=varCno, width=16)
    entryCno.grid(row=1, column=2, pady=10, padx=5)
    # 创建排序按钮
    buttonSort = tkinter.Button(frmd, text="排序", command=lambda: sortsql(varCno.get()))
    buttonSort.grid(row=2, column=1, padx=100, pady=5, columnspan=2, sticky='nesw')


# 查询学生对应界面和函数
def findstu(sno):
    print("查询学生信息")
    for widget in frmd.winfo_children():
        widget.grid_forget()
    # 连接数据库
    with connect() as cnx:
        # 创建游标对象
        cursor = cnx.cursor()

        try:
            #根据学号查询学生信息
            findSQL = "SELECT * FROM student WHERE Sno='%s'" % sno
            # 执行 SQL 语句
            cursor.execute(findSQL)

            # 获取所有结果行
            rows = cursor.fetchall()
            # 输出结果
            for row in rows:
                print(row)
                # 创建文本框
                scrollbar_x = tkinter.Scrollbar(frmd, orient=tkinter.HORIZONTAL)
                scrollbar_y = tkinter.Scrollbar(frmd, orient=tkinter.VERTICAL)
                tree = ttk.Treeview(frmd, columns=("Sno", "Name", "Sex", "Age", "Sdept"),
                                    yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
                scrollbar_x.config(command=tree.xview)
                scrollbar_y.config(command=tree.yview)

                tree.heading("#0", text="ID")
                tree.heading("Sno", text="学号")
                tree.heading("Name", text="姓名")
                tree.heading("Sex", text="性别")
                tree.heading("Age", text="年龄")
                tree.heading("Sdept", text="专业")

                tree.column("#0", width=50)
                tree.column("Sno", width=100)
                tree.column("Name", width=50)
                tree.column("Sex", width=50)
                tree.column("Age", width=50)
                tree.column("Sdept", width=100)
                tree.column("#0", width=0, stretch=tkinter.NO)
                tree.grid(row=3, column=1, sticky=tkinter.NSEW, columnspan=2)

                scrollbar_x.grid(row=3, column=1, sticky=tkinter.EW)
                scrollbar_y.grid(row=3, column=1, sticky=tkinter.NS)
                # 将查询结果添加到表格中
                tree.insert("", tkinter.END, values=row)

        except Exception as e:
            # 发生异常时，回滚事务
            cnx.rollback()
            print("Failed to execute SQL: ", e)

        else:
            # 提交事务
            cnx.commit()
            print("Data found successfully!")

        finally:
            # 关闭游标和连接对象
            cursor.close()


# 查询学生选课对应和函数界面
def findsc(sno):
    print("查询学生选课信息")
    for widget in frmd.winfo_children():
        widget.grid_forget()
    # 创建表格组件
    scrollbar_x = tkinter.Scrollbar(frmd, orient=tkinter.HORIZONTAL)
    scrollbar_y = tkinter.Scrollbar(frmd, orient=tkinter.VERTICAL)
    tree = ttk.Treeview(frmd, columns=("Cno", "Cname"), yscrollcommand=scrollbar_y.set,
                        xscrollcommand=scrollbar_x.set)
    scrollbar_x.config(command=tree.xview)
    scrollbar_y.config(command=tree.yview)

    tree.heading("#0", text="ID")
    tree.heading("Cno", text="课程号")
    tree.heading("Cname", text="课程名")

    tree.column("#0", width=70)
    tree.column("Cno", width=70)
    tree.column("Cname", width=150)
    tree.column("#0", width=0, stretch=tkinter.NO)
    tree.grid(row=1, sticky=tkinter.NSEW, columnspan=3)

    scrollbar_x.grid(row=1, column=1, sticky=tkinter.EW)
    scrollbar_y.grid(row=1, column=1, sticky=tkinter.NS)
    # 连接数据库
    with connect() as cnx:
        # 创建游标对象
        cursor = cnx.cursor()

        try:
            # 定义一个SQL查询语句，用于从sc表和course表中联接查询课程号和课程名
            # 其中%s是一个占位符，用于后续通过参数传递学生编号(sno)
            findSQL = "SELECT sc.Cno, course.Cname " \
                      "FROM sc JOIN course ON sc.Cno=course.Cno WHERE sc.Sno=%s"
            # 执行 SQL 语句
            cursor.execute(findSQL, (sno,))

            # 获取所有结果行
            rows = cursor.fetchall()
            # 清空表格
            tree.delete(*tree.get_children())

            # 将查询结果添加到表格中
            for row in rows:
                tree.insert("", tkinter.END, values=row)

        except Exception as e:
            # 发生异常时，回滚事务
            cnx.rollback()
            print("Failed to execute SQL: ", e)

        else:
            # 提交事务
            cnx.commit()
            print("Data found successfully!")

        finally:
            # 关闭游标和连接对象
            cursor.close()


# 根据课程名获课程号的函数
def get_cno(cname):
    with connect() as cnx:
        try:
            # 创建游标对象
            cursor = cnx.cursor()

            # 定义查询语句，用于从course表中根据课程名查询课程号
            query = "SELECT Cno FROM course WHERE Cname=%s"

            # 执行查询语句，并将cname作为参数传入
            cursor.execute(query, cname)

            # 获取查询结果，结果为元组（Cno,）
            result = cursor.fetchone()

            # 获取元组中的第一个字段Cno，通过索引或元素名访问
            cno = result[0]

            # 如果查询结果不为None，则返回查询到的Cno，否则返回None
            if result:
                return result[0]  # 返回查询到的Cno字段

        except Exception as e:
            # 发生异常时，回滚事务并记录错误信息
            cnx.rollback()
            error = "Error in get_cno(): " + str(e)
            print(error)
            with open('error.log', 'a') as f:
                f.write(error + '\n')

        else:
            # 提交事务
            cnx.commit()

        finally:
            # 关闭游标和连接对象
            cursor.close()


# 判断学生是否选修了先行课的函数
def has_taken_prerequisite(sno, pno):
    with connect() as cnx:
        try:
            # 创建游标对象
            cursor = cnx.cursor()

            # 查询选课表，检查该学生是否已选该前置课程
            query = "SELECT * FROM sc WHERE Sno=%s AND Cno=%s"
            cursor.execute(query, (sno, pno))
            result = cursor.fetchone()

            return result is not None  # 如果result不是None，说明该学生已选该前置课程，因此返回True；如果result是None，说明该学生未选该前置课程，返回False。

        except Exception as e:
            # 发生异常时，回滚事务
            cnx.rollback()
            print("Failed to execute SQL: ", e)

        finally:
            # 关闭游标和连接对象
            cursor.close()


# 将选课情况添加到数据库
def add_sc(sno, index):
    # 获取选择的课程名称
    select_course = index

    # 根据课程名称获取课程号
    cno = get_cno(select_course)

    with connect() as cnx:
        try:
            # 创建游标对象
            cursor = cnx.cursor()

            # 判断是否已选当前课程
            query = "SELECT * FROM sc WHERE Sno=%s AND Cno=%s"
            cursor.execute(query, (sno, cno))
            result = cursor.fetchone()

            if result:
                # 如果已选该门课程，弹出提示信息
                tkinter.messagebox.showwarning('选课失败', '您已经选择了该门课程！')
            else:
                # 查询课程的前置课程号
                query_pno = "SELECT Cpno FROM course WHERE Cno=%s"
                cursor.execute(query_pno, (cno,))
                pno = cursor.fetchone()
                if pno is None:
                    # 没有前置课程，可以直接选课
                    pass
                else:
                    # 有前置课程，需要检查是否已修
                    prerequisite_course = pno[0]  # 假设 Cpno 是查询结果的第一列
                    if prerequisite_course is not None:
                        # 如果该课程有前置课程，则检查学生是否已选该前置课程
                        has_taken_pno = has_taken_prerequisite(sno, prerequisite_course)
                        if not has_taken_pno:
                            # 如果学生未选该前置课程，则提醒学生并返回
                            tkinter.messagebox.showwarning(
                                '选课失败', '您未选修该课程的前置课程，不能选修该课程！'
                            )
                            return

                # 将选课信息插入到选课表中
                add_choice = "INSERT INTO sc(Sno, Cno) VALUES(%s, %s)"
                cursor.execute(add_choice, (sno, cno))
                tkinter.messagebox.showinfo('选课成功', '选课成功！')

        except Exception as e:
            # 发生异常时，回滚事务
            cnx.rollback()
            print("Failed to execute SQL: ", e)

        else:
            # 提交事务
            cnx.commit()

        finally:
            # 关闭游标和连接对象
            cursor.close()


# 选课和退课的界面
def choice(sno):
    for widget in frmd.winfo_children():
        widget.grid_forget()
    with connect() as cnx:
        # 创建游标对象
        cursor = cnx.cursor()

        try:
            # 执行 SQL 语句
            find_course = "SELECT Cname FROM course"
            cursor.execute(find_course)

            # 获取所有结果行
            rows = cursor.fetchall()
            # 创建列表框
            listbox_course = tkinter.Listbox(frmd, selectmode='SINGLE')
            # 初始化列表框
            items = rows
            for item in items:
                listbox_course.insert(tkinter.END, item)
            listbox_course.grid(row=1, column=1)

            def choose(sno):
                index = listbox_course.curselection()
                if len(index) > 0:
                    add_sc(sno, listbox_course.get(index))  # 有选中项时添加到数据库
                else:
                    # 弹出消息框显示没有选中项
                    tkinter.messagebox.showwarning('选择失败', '请选择一个课程！')

            def select_and_drop(sno):
                # 检索用户选择的课程号
                index = listbox_course.curselection()
                if len(index) > 0:
                    cno = get_cno(listbox_course.get(index))  # 假设get_cno函数能够根据课程名获取课程号
                    drop_course(sno, cno)  # 调用退课函数
                else:
                    messagebox.showwarning('选择失败', '请选择一个课程来退选！')


            # 创建选课按钮
            button_course = tkinter.Button(frmd, text="选课", command=lambda: choose(sno))
            button_course.grid(row=2, column=2)
            # 创建退课按钮
            button_drop = tkinter.Button(frmd, text="退课", command=lambda: select_and_drop(sno))
            button_drop.grid(row=3, column=2)  # 假设这是合适的行和列位置

            for row in rows:
                print(row)


        except Exception as e:
            # 发生异常时，回滚事务
            cnx.rollback()
            # 清空列表框
            listbox_course.delete(0, tkinter.END)
            # 弹出错误提示框并记录错误信息
            error = "Error in choice(): " + str(e)
            tkinter.messagebox.showerror('Error', error)
            print(error)
            # print("Failed to execute SQL: ", e)

        else:
            # 提交事务
            cnx.commit()
            print("Data updata successfully!")

        finally:
            # 关闭游标和连接对象
            cursor.close()

#退课函数及界面
def drop_course(sno, cno):
    # 弹出确认对话框
    result = messagebox.askyesno("确认退课", f"您确定要退选课程号 {cno} 吗？")
    if result:
        # 执行退课操作（连接到数据库，执行DELETE语句）
        with connect() as cnx:
            cursor = cnx.cursor()
            try:
                del_sql = "DELETE FROM sc WHERE Sno=%s AND Cno=%s"
                cursor.execute(del_sql, (sno, cno))
                cnx.commit()
                # 更新UI或显示消息
                messagebox.showinfo("退课成功", "课程退选成功！")
            except Exception as e:
                cnx.rollback()
                messagebox.showerror("退课失败", f"退课失败：{e}")





# 管理员登录事件处理函数
def admin():
    # 移除登录窗口的所有组件
    for widget in frma.winfo_children():
        widget.grid_forget()
    # 移除画布上的图片
    canvas_root.pack_forget()
    # 更改窗口大小及其他属性
    win.geometry("960x680")
    win.title("天命——圣芙蕾雅学园选课系统")
    win.resizable(True, True)
    frmb.config(height=20)
    frmb.destroy()

    # 创建listbox组件
    listbox = tkinter.Listbox(frmc, selectmode='SINGLE')
    items = ["添加学生信息", "查询学生信息", "修改学生信息", "删除学生信息", "学生成绩录入", "依据学生成绩排序"]
    for item in items:
        listbox.insert(tkinter.END, item)
    listbox.pack(side="left", expand=1, fill='y')
    listbox.config(height=600)

    def handle_selection(event):
        # 检索所选项目的索引
        index = listbox.curselection()
        # 如果有项目被选择，则执行特定操作
        if index:
            # 获取所选项目的文本
            selection = listbox.get(index)
            if selection == items[0]:
                add()
                logger.info("admin 添加学生信息")
            if selection == items[1]:
                find()
                logger.info("admin 查询学生信息")
            if selection == items[2]:
                updata()
                logger.info("admin 修改学生信息")
            if selection == items[3]:
                delete()
                logger.info("admin 删除学生信息")
            if selection == items[4]:
                upgrade()
                logger.info("admin 录入学生成绩")
            if selection == items[5]:
                sort()
                logger.info("admin 依据成绩排序")

    # 将Listbox绑定到选择事件
    listbox.bind("<<ListboxSelect>>", handle_selection)


# 普通学生登录事件处理函数
def user(sno):
    print("用户登录")
    # 移除登录窗口的所有组件
    for widget in frma.winfo_children():
        widget.grid_forget()
    # 移除画布上的图片
    canvas_root.pack_forget()
    # 更改窗口大小及其他属性
    win.geometry("960x680")
    win.title("学生管理系统")
    win.resizable(True, True)
    # 移除frmb框架
    frmb.destroy()

    # 创建listbox组件
    listbox = tkinter.Listbox(frmc, selectmode='SINGLE')
    items = ["查询学生信息", "查询选课信息", "选课", "查看成绩信息"]
    for item in items:
        listbox.insert(tkinter.END, item)
    listbox.pack(side="left", expand=1, fill='y')
    listbox.config(height=600)

    def handle_selection(event):
        # 检索所选项目的索引
        index = listbox.curselection()
        # 如果有项目被选择，则执行特定操作
        if index:
            # 获取所选项目的文本
            selection = listbox.get(index)
            if selection == items[0]:
                findstu(sno)
                logger.info(f"{sno}查询学生本人基本信息")
            if selection == items[1]:
                findsc(sno)
                logger.info(f"{sno}查询学生本人选信息")
            if selection == items[2]:
                choice(sno)
                logger.info(f"{sno}添加学生本人的选课信息")
            if selection == items[3]:
                findgrade(sno)
                logger.info(f"{sno}查询学生本人成绩信息")

    # 将Listbox绑定到选择事件
    listbox.bind("<<ListboxSelect>>", handle_selection)


# 登录按钮的事件处理函数
def login():
    m = Username.get()
    n = Password.get()
    # 查询数据库 - 检索给定用户名和密码所对应的用户角色信息
    sql = "SELECT role FROM user_info WHERE username=%s AND password=%s"
    con = connect()
    cursor = con.cursor()
    cursor.execute(sql, (m, n))
    result = cursor.fetchone()
    # 关闭数据库连接
    cursor.close()
    con.close()

    # 判断用户角色并跳转到对应页面，如果用户不存在或者密码错误，弹出登录失败提示框。
    if result and result[0] == 'admin':
        # 获取当前日期和时间
        now = datetime.datetime.now()
        # 将日期和时间转换为所需的格式
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        # 输出当前时间
        print(current_time + "  登录成功")
        logger.info(f"{m}登录成功")
        admin()
        return ['admin']
    elif result and result[0] == 'user':
        # 获取当前日期和时间
        now = datetime.datetime.now()
        # 将日期和时间转换为所需的格式
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        # 输出当前时间
        print(current_time + "  登录成功")
        logger.info(f"{m}登录成功")
        user(m)
        return ['user', m]
    else:
        # 弹出消息框显示登录失败
        tkinter.messagebox.showwarning('登录失败', '用户名或密码错误，请重试！')
        return None


# 设置日志输出格式和级别
logging.basicConfig(filename='output.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# 创建主窗口
win = tkinter.Tk()
win.title("登录界面")
win.geometry("430x330")

# 创建顶部框架
frma = tkinter.Frame(win)
frma.pack(side="bottom")

frmc = tkinter.Frame(win)
frmc.pack(side='left')  # 左
frmd = tkinter.Frame(win)
frmd.pack(side='top')  # 右
# 创建用户名输入框
str1 = tkinter.StringVar(value="")
Username = tkinter.Entry(frma, textvariable=str1, width=20)
Username.grid(row=0, column=1, padx=10, pady=5)
Ulabel = tkinter.Label(frma, text="用户名：")
Ulabel.grid(row=0, column=0, pady=5, padx=10)

# 创建密码输入框
str2 = tkinter.StringVar(value="")
Password = tkinter.Entry(frma, textvariable=str2, width=20, show='*')
Password.grid(row=1, column=1, pady=5, padx=10)
PLabel = tkinter.Label(frma, text="密码：")
PLabel.grid(row=1, column=0, padx=10, pady=5)

# 创建重置按钮和登录按钮
resbtn = tkinter.Button(frma, text="重置", command=cancel)
resbtn.grid(row=2, column=0, padx=10, pady=5)
logbtn = tkinter.Button(frma, text="登录", command=login)
logbtn.grid(row=2, column=1, padx=10, pady=5)

# 创建底部框架
frmb = tkinter.Frame(win)
frmb.pack(side="top")


# 打开指定的图片文件，缩放至指定尺寸
def get_image(filename, width, height):
    im = Image.open(filename).resize((width, height))
    return ImageTk.PhotoImage(im)


# 创建画布，设置要显示的图片，把画布添加至应用程序窗口
canvas_root = tkinter.Canvas(frmb, width=430, height=207)
im_root = get_image('background.png', 430, 207)
canvas_root.create_image(215, 104, image=im_root)
canvas_root.pack()

win.resizable(False, False)






# 进入主循环
win.mainloop()
