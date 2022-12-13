#if !defined(NODE_INCLUDED)
#define NODE_INCLUDED 1
struct Node {
    int val;
    
    Node(int X = 0)
        :val(X) {}

    bool operator != (const Node& P) const {
        return val != P.val;
    }
    bool operator < (const Node& P) const {
        return val < P.val;
    }
    bool operator <= (const Node& P) const {
        return val <= P.val;
    }
    bool operator > (const Node& P) const {
        return val > P.val;
    }
    Node operator - () const {
        return Node{-val};
    }
    Node operator + (const Node &a) const {
        return Node{val + a.val};
    }
    Node operator - (const Node &a) const {
        return Node{val - a.val};
    }
    Node operator * (const int &f) const {
        return Node{val * f};
    }
};
#endif

#if !defined(MYLIB_INCLUDED)
#define MYLIB_INCLUDED 1

#include <bits/stdc++.h>


#endif

#if !defined(MYLIB_CONSTANTS_H)
#define MYLIB_CONSTANTS_H 1

using namespace std;
typedef long long ll;
typedef pair<ll, ll> pll;
typedef pair<int, int> pii;
typedef pair<pii, int> piii;

const ll MOD = 1e9 + 7;
const int inf = 0x3f3f3f3f;

// 在虚拟机环境会导致 Out of memory
// const int MAXM = 30;
// const int MAXN = 1e6 + 5;
// const int MAXT = 1e6 + 5;

const int MAXM = 10;
const int MAXN = 1e4 + 5;
const int MAXT = 1e4 + 5;

#endif

// for saving cache file
extern int period;
extern int times;

extern int N, M, K; // Total Block = K * 100 * M
extern int seed_num;
extern int global_cost[MAXN];
extern int dn[MAXN][MAXM];
extern int PROCESS_DELAY;
extern int ZIPF_range;
extern double ZIPF_alpha;

extern Node local_profit[MAXM][MAXN], global_profit[MAXN];
extern int storages[MAXM];
extern ll ori_payment;
extern ll tot_req;
void init();
void init_para();
void set_MEC_size(int);
void output_lp_file();

/**
Answer: 2851785 2512225
Answer: 74191 53540

int N = 100000, M = 5, K = 50000;
8.310 s
4.977 s 修改 contain 为顺序表
1.561 s 只有 floyd
4.234 s 修改 mec_nvalue 为排序表
3.295 s 改 dijkstra

int N = 62400 , M = 3, K = 5000;
0.4 s

int N = 1000, M = 30, K = 300;
6.006 s
4.082 s 只有 floyd

int N = 1000000, M = 10, K = 500000;
init() Time: 404 ms
Set Up Time: 8364 ms
T: 5000000
Total Path Length: 10621639
Answer: 58021834 51008816
fsp() Time: 143867 ms

int N = 500000, M = 10, K = 500000;
init() Time: 210 ms
Set Up Time: 3969 ms
T: 5000000
There is no path exist, T: 1493891
Total Path Length: 7012216
Answer: 30036792 30009785
fsp() Time: 86071 ms

int N = 500000, M = 10, K = 100000;
init() Time: 225 ms
Set Up Time: 4009 ms
T: 1000000
Total Path Length: 2227660
Answer: 21838460 19151001
fsp() Time: 34390 ms

int N = 1000000, M = 10, K = 100000;
init() Time: 410 ms
Set Up Time: 8353 ms
T: 1000000
Total Path Length: 2236304
Answer: 35843071 33539851
fsp() Time: 42195 ms


int N = 500000, M = 15, K = 20000;
srand(28);
Answer: 203172948 175487509
        203172944 175489292

int N = 1000000, M = 10, K = 500000;
1654434818
init() Time: 415 ms
Set Up Time: 11962 ms
T: 5000000
Total Path Length: 10038726
Answer: 439950853 371377570
fsp() Time: 84391 ms
*/
