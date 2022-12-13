M = 3
N = 200
PERIOD = 10 # 10s

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
CACHE_TXT = './data/ksp_cache_10_0.txt'
CACHE_JSON = './data/cache.json'

# 解析请求文件
P_PATH = './data'
DN_FILE = 'dn_10_1.txt'


SINGAL_FILE = './data/signal.txt'
VIDEO_FILE = './data/conference.mp4'

# 计算时延节省量
CLOUD_RES_FILE = './data/10.0.%s.2_cloud.txt'
KSP_RES_FILE = './data/10.0.%s.2_ksp.txt'
DIS_RES_FILE = './data/10.0.%s.2_dis.txt'
SELF_RES_FILE = './data/10.0.%s.2_self.txt'
MIXCO_RES_FILE = './data/10.0.%s.2_mixco.txt'

