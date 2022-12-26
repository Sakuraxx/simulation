M = 3
N = 100
PERIOD = 1 # 1s
TOT_P = 10
T = 10 # 轮数

CLOUD_IP = "10.0.200.254"
MEC_IP = '10.0.%s.1'
CLIENT_IP = '10.0.%s.2'
CLOUD_CACHE = "cloud"

# tile 大小
_1KB = 1024
_1MB = 1024 * 1024
TILE_SIZE = _1KB

# 链路带宽 Mbit
_1MB_TOPO = 1
UM_BW = _1MB_TOPO * 10
MM_BW = _1MB_TOPO * 100
MD_BW = _1MB_TOPO * 1000

# 延迟
UM_DELAY = '1ms'
MM_DELAY = '2ms'
MD_DELAY = '50ms'

# 解析缓存文件
CACHE_MODE = ('ksp', 'distributed', 'selfTop', 'mixco')
CACHE_TXT = './data/ori_cache/%s_cache_%s_%s.txt'
CACHE_JSON = './data/cache/%s_cache_%s_%s.json' # ksp_cache_10_0.json

# 解析请求文件
DN_FILE = './data/dn/%s/%s' # /data/dn/1/0 时间间隔为1第0轮
REQ_ROOT = './data/req'
REQ_FILE = './data/req/%s_%s_%s.json' # 10.0.0.2_10_1.txt
RES_FILE = './data/res/%s_%s_%s_%s.txt' # 10.0.0.2_ksp_10_1.txt

SINGAL_FILE = './data/signal.txt'
VIDEO_FILE = './data/conference.mp4'

# 计算时延节省量
DELAY_RES_FILE = './data/res/10.0.%s.2_%s_%s_%s.txt' # 10.0.0.2_ksp_10_1.txt

ANS_FILE = './data/ans/ans.json'
RES_JSON_FILE = './data/res/peroid_%s.json' # peroid_1.json