from constant import *

# 计算时延节省量

def cal_profit(filename):
    res = 0
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            fields = line.split(' ')
            res += int(fields[-1])
    return res

def wc_count(file_name):
    import subprocess
    out = subprocess.getoutput("wc -l %s" % file_name)
    return int(out.split()[0])

def main():
    cloud_res = 0
    ksp_res = 0
    cnt = 0
    for j in range(M):
        cloud_res += cal_profit(CLOUD_RES_FILE % j)
        ksp_res += cal_profit(KSP_RES_FILE % j)
        cnt += wc_count(KSP_RES_FILE % j)
    profit = ((cloud_res - ksp_res) / cnt) / (cloud_res / cnt)
    print(profit)

if __name__ == '__main__':
    main()