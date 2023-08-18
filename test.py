
import multiprocessing
def temp(ins_name):
    print(ins_name)
    print('hello world')
    return 0
pool = multiprocessing.Pool(processes=4)
pool.map(temp, range(10))
pool.close()
pool.join()