
import sqlite3

conn = sqlite3.connect('stock.db')

c = conn.cursor()

def insert_prod(name,q,cost,date):
    with conn:
        c.execute("SELECT quantity FROM stock WHERE name = :name",{'name':name})
        check = c.fetchone()

    #print(check)
    if check is None:
        with conn:
            #print('yes')
            c.execute("INSERT INTO stock VALUES (:name, :quantity, :cost)", {'name': name, 'quantity': q, 'cost': cost})
            a = name.upper() +' ' +str(q)+' '+str(cost)+' '+str(date) + ' ' + 'INSERT '+"\n"
            with open("transaction.txt", "a") as myfile:
                myfile.write(a)
        return 'Inserted the stock in DataBase'
    else:
        return 'Stock with same name already present.'

def show_stock():
    with conn:
        c.execute("SELECT * FROM stock")

    cursor=conn.execute("select name,quantity from stock")
    ll=[]
    for i in cursor:
        ll.append([i[0],i[1]])

    import matplotlib.pyplot as plt
    import pandas as pd

    ll.sort(key=lambda e:e[1],reverse=False)
    item=[]
    quan=[]
    for i in ll:
        item.append(i[0])
        quan.append(i[1])
        
    df=pd.DataFrame(quan,item)
    df.plot.bar()
    plt.xlabel('item')
    plt.ylabel('quantity')
    plt.show()

    return c.fetchall()
'''def show_stock():
    with conn:
        c.execute("SELECT * FROM stock")

    return c.fetchall()'''


def update_cost(name, cost,date):
    with conn:
        c.execute("""UPDATE stock SET cost = :cost
                    WHERE name = :name""",
                  {'name': name, 'cost': cost})


def update_quantity(name, val,date):
    with conn:
        c.execute("SELECT quantity FROM stock WHERE name = :name",{'name': name})
        z = c.fetchone()
        cost = z[0]+val
        if cost < 0:
            return
        c.execute("""UPDATE stock SET quantity = :quantity
                    WHERE name = :name""",
                  {'name': name, 'quantity': cost})
        a = name.upper() + ' ' + str(z[0]) + ' ' + str(cost) + ' ' + str(date) +' UPDATE '+"\n"
        with open("transaction.txt", "a") as myfile:
            myfile.write(a)


def remove_stock(name,date):
    with conn:
        c.execute("DELETE from stock WHERE name = :name",
                  {'name': name})
        a = name.upper() + ' ' + 'None' + ' ' + 'None'+' ' + str(date) + ' REMOVE '+"\n"

        with open("transaction.txt", "a") as myfile:
            myfile.write(a)

        conn.commit()

#conn.close()