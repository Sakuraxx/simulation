#include "../include/ksp.h"
#include "../include/data.h"

// for saving cache file
extern int period;
extern int times;

extern Node local_profit[MAXM][MAXN], global_profit[MAXN];
extern int storages[MAXM];

int cnt[MAXN];
pair<Node, int> mec_nvalue[MAXM][MAXN];
int nvalue_ind[MAXM];

__gnu_pbds::priority_queue<pair<Node, int>, greater<pair<Node, int> >,
                           pairing_heap_tag> mec_pq[MAXM][MAXM];
int remain[MAXM];
bool contain[MAXM][MAXN];
bool debug = false;
pair<Node, int> d[MAXM][MAXM];
Node pi[MAXM];
ll ans;

Node vals(int ind, int j, int f) {
    return global_profit[ind] * f + local_profit[j][ind];
}

void set_G() {
    d[0][M + 1] = {Node{inf}, -1};
    for(int di = 1; di <= M; di++) {
        int i = di - 1;
        pair<Node, int> best_val = {Node{inf}, -1};
        if(nvalue_ind[i]) {
            best_val = mec_nvalue[i][ nvalue_ind[i] - 1 ];
            best_val = {-best_val.first, best_val.second};
        }

        d[0][di] = best_val;
        d[di][M + 1] = {Node{inf}, -1};
        if(remain[i]) d[di][M + 1] = {Node{0}, -1};
        for(int dj = 1; dj <= M; dj++) {
            int j = dj - 1;
            d[di][dj] = {Node{inf}, -1};
            if(i == j) continue;
            while(!mec_pq[i][j].empty()) {
                pair<Node, int> pq_top = mec_pq[i][j].top();
                if(!(contain[i][pq_top.second] && !contain[j][pq_top.second])) {
                    mec_pq[i][j].pop();
                    continue;
                }
                d[di][dj] = {pq_top.first, pq_top.second};
                break;
            }
        }
    }
}

void set_pi(int m) {
    pi[0] = Node{0};
    for(int k = 0; k < m; k++)
        for(int i = 0; i < m; i++)
            for(int j = 0; j < m; j++)
                if (d[i][j].first > d[i][k].first + d[k][j].first)
                    d[i][j] = {d[i][k].first + d[k][j].first, d[i][k].second};

    for(int i = 1; i < m; i++) pi[i] = d[0][i].first;
}

bool vis[MAXN];
Node dis[MAXN];
int pre[MAXM];
void dijkstra(int m) {
    fill(dis, dis + m, Node(inf));
    fill(vis, vis + m, false);
    dis[0] = Node{0};

    while(true) {
        int v = -1;
        for(int i = 0; i < m; i++) {
            if(!vis[i] && (v == -1 || dis[i] < dis[v])) v = i;
        }
        if(v == -1) break;
        vis[v] = true;

        for(int i = 0; i < m; i++) {
            Node w = d[v][i].first + pi[v] - pi[i];
            if(w < Node{0}) {
                printf(" %d %d %d\n", v, i, w.val);
            }
            if (dis[i] > dis[v] + w) {
                dis[i] = dis[v] + w;
                pre[i] = v;;
            }
        }
    }
}

vector<pii> getPath(int e) {
    vector<pii> path;
    while (e) {
        path.push_back({pre[e] - 1, d[ pre[e] ][e].second});
        e = pre[e];
    }
    reverse(path.begin(), path.end());
    return path;
}

long long fsp() {
    // clock_t t1 = clock();
    ans = 0;
    for(int i = 0; i < M + 2; i++)
        for(int j = 0; j < M + 2; j++)
            d[i][j] = {Node{inf}, -1};

    for(int i = 0; i < N; i++) cnt[i] = 0;
    for(int j = 0; j < M; j++) {
        nvalue_ind[j] = 0;
        remain[j] = storages[j];
        for(int i = 0; i < N; i++) {
            contain[j][i] = false;
            mec_nvalue[j][ nvalue_ind[j]++ ] = {vals(i, j, 0), i};
            mec_nvalue[j][ nvalue_ind[j]++ ] = {vals(i, j, 1), i};
        }
        sort(mec_nvalue[j], mec_nvalue[j] + nvalue_ind[j]);
        for(int k = 0; k < M; k++) mec_pq[j][k].clear();
    }

    set_G();
    set_pi(M + 2);

    // 确定最小 T
    int T = 0;
    for(int i = 0; i < M; i++) T += storages[i];
    T = min(M * N, T);

    int totPathLen = 0;
    // printf("Set Up Time: %ld ms\n", clock() - t1);
    // t1 = clock();
    // printf("T: %d\n", T);

    while(T--) {
        for(int j = 0; j < M; j++) {
            while(nvalue_ind[j]) {
                pair<Node, int> init_val = mec_nvalue[j][ nvalue_ind[j] - 1 ];
                int ind = init_val.second;
                if (cnt[ind]) {
                    Node local_benefit = Node{local_profit[j][ind]};
                    // 若已经在别处存下了 或 以及存下了内容 ind
                    if (init_val.first != local_benefit || contain[j][ind]) {
                        nvalue_ind[j]--;
                        continue;
                    }
                }
                break;
            }
        }

        set_G();
        dijkstra(M + 2);
        Node mi = -(dis[M + 1] + pi[M + 1] - pi[0]);
        if(mi < Node{0}) {
            printf("There is no path exist, T: %d\n", T);
            break;
        }

        for(int i = 0; i < M + 2; i++) {
            pi[i] = pi[i] + dis[i];
            pi[i] = min(pi[i], Node{inf});
        }

        vector<pii> path = getPath(M + 1);

        totPathLen += path.size();

        cnt[path[0].second] += 1;
        remain[path[ path.size() - 1 ].first] -= 1;
        nvalue_ind[path[1].first]--;
        for(int i = 1; i < (int)path.size(); i++) {
            int mec_add = path[i].first;
            int item = path[i - 1].second;
            contain[mec_add][item] = true;
            for(int j = 0; j < M; j++) {
                if(j == mec_add) continue;
                if(!contain[j][item]) {
                    Node val = vals(item, mec_add, 0) - vals(item, j, 0);
                    mec_pq[mec_add][j].push({val, item});
                }
            }
            if(i != 1) {
                int mec_remove = path[i - 1].first;
                contain[mec_remove][item] = false;
                for(int j = 0; j < M; j++) {
                    if(j == mec_remove) continue;
                    if(contain[j][item]) {
                        Node val = vals(item, j, 0) - vals(item, mec_remove, 0);
                        mec_pq[j][mec_remove].push({val, item});
                    }
                }
            }
        }

        ans += mi.val;
    }
    // printf("Total Path Length: %d\n", totPathLen);
    // printf("Answer: %lld\n", ans);
    // printf("fsp() Time: %ld ms\n", clock() - t1);
    // printf("\n");

    // 记下KSP的缓存分布
    fstream ksp_cache;
    stringstream s;
    s << "../data/ori_cache/ksp_cache_" << period << "_" << times << ".txt";
    ksp_cache.open(s.str(), ios::out);  // write,清空再写入
    if (ksp_cache.is_open())
    {
        for(int j = 0; j < M; j++) {
            for(int i = 0; i < N; i++) {
                ksp_cache << j << " " << i << " " << contain[j][i] << "\n";
            }
        }
    } else {
        printf("open failed.\n");
    }
    ksp_cache.close();


    return ans;
}
