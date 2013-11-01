
def writeTo(path,data,mode):
    f = file(path,mode)
    f.write(data)
    f.close()