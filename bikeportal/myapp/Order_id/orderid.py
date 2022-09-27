
def generate_id():
    r = open(r"C:\Users\HAMZA\bikeportal\myapp\order_id\id.txt","r")
    con = r.read()
    print(con)
    newint = int(con)
    v = newint+1
    print(v)
    w = open(r"C:\Users\HAMZA\bikeportal\myapp\order_id\id.txt", "w+")
    newstr = str(v)
    print(newstr)
    w.write(newstr)
    w.close()
    ty = "A-"+con
    return ty
a = generate_id()