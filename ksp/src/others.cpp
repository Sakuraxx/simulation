#include "../include/others.h"

using namespace std;

// for saving cache file
extern int period;
extern int times;

bool cache[MAXM][MAXN];
bool mixco_cache[MAXM][MAXN];
int dis_sz[MAXM];
pair<Node, int> arr[MAXM][MAXN];
int arr_ind[MAXN];
bool mixco = false;
bool dis_cnt[MAXN];
int dis_remain[MAXM];
priority_queue<pair<Node, pii> > pq;

ll cal_profile() {
    ll ans = 0;
    for(int i = 0; i < N; i++) {
        bool flag = false;
        for(int j = 0; j < M; j++) {
            if(cache[j][i]) {
                ans += local_profit[j][i].val;
                flag = true;
            }
        }
        if(flag) ans += global_profit[i].val;
    }
    return ans;
}

// 记下缓存分布
void save_cache_to_file(int alog) {
    fstream cache_file;
    string filename;
    if(alog == 1) filename = "../data/ori_cache/selfTop_cache_";
    else if (alog == 2) filename = "../data/ori_cache/distributed_cache_";
    else if (alog == 3) filename = "../data/ori_cache/mixco_cache_";
    stringstream s;
    s << filename << period << "_" << times << ".txt";
    cache_file.open(s.str(), ios::out);  // write,清空再写入
    if (cache_file.is_open())
    {
        for(int j = 0; j < M; j++) {
            for(int i = 0; i < N; i++) {
                if(alog == 1 || alog == 2)
                    cache_file << j << " " << i << " " << cache[j][i] << "\n";
                else
                    cache_file << j << " " << i << " " << mixco_cache[j][i] << "\n";
            }
        }
    } else {
        printf("other open failed.\n");
    }
    cache_file.close();
}

ll get_self_top_profit() {
    for(int j = 0; j < M; j++) {
        fill(cache[j], cache[j] + N, false);
        for(int i = 0; i < N; i++) arr[j][i] = {local_profit[j][i], i};
        sort(arr[j], arr[j] + N, greater<pair<Node, int> >());
        for(int i = 0; i < min(storages[j], N); i++) {
            cache[j][arr[j][i].second] = true;
        }
    }
    save_cache_to_file(1);
    return cal_profile();
}

int distributed_choose_max(int tile_ind) {
    int mx_ind = -1;
    for(int j = 0; j < M; j++) {
        if(!dis_remain[j] || (mixco && mixco_cache[j][tile_ind])) continue;
        if(mx_ind == -1 || local_profit[mx_ind][tile_ind] < local_profit[j][tile_ind]) {
            mx_ind = j;
        }
    }
    return mx_ind;
}

ll get_distributed_profit() {
    while(!pq.empty()) pq.pop();
    for(int j = 0; j < M; j++) {
        dis_remain[j] = mixco ? dis_sz[j] : storages[j];
        fill(cache[j], cache[j] + N, false);
    }

    // 所有内容存在收益最高的 MEC 上
    for(int i = 0; i < N; i++) {
        dis_cnt[i] = 0;
        int mx_ind = distributed_choose_max(i);
        if(mx_ind == -1) continue;
        pq.push({local_profit[mx_ind][i] + global_profit[i], {mx_ind, i}});
    }

    while(!pq.empty()) {
        int mec_ind = pq.top().second.first;
        int tile_ind = pq.top().second.second;
        pq.pop();
        if(dis_cnt[tile_ind]) continue;
        if(!dis_remain[mec_ind]) {
            int mx_ind = distributed_choose_max(tile_ind);
            if(mx_ind == -1) break;
            pq.push({local_profit[mx_ind][tile_ind] + global_profit[tile_ind], {mx_ind, tile_ind}});
            continue;
        }
        dis_cnt[tile_ind] = true;
        dis_remain[mec_ind]--;
        cache[mec_ind][tile_ind] = true;
    }
    save_cache_to_file(2);
    return cal_profile();
}

ll get_mixco_profit() {
    // init
    mixco = true;
    for(int i = 0; i < N; i++) arr_ind[i] = 0;
    for(int j = 0; j < M; j++) {
        fill(cache[j], cache[j] + N, false);
        fill(mixco_cache[j], mixco_cache[j] + N, false);
        for(int i = 0; i < N; i++) arr[j][i] = {local_profit[j][i], i};
        sort(arr[j], arr[j] + N, greater<pair<Node, int> >());
        dis_sz[j] = storages[j];
    }

    // self-top
    ll res_profile = get_distributed_profit();
    ll self_profile = 0;
    while(true) {
        ll mx_profile = 0;
        int mx_ind = -1;
        for(int j = 0; j < M; j++) {
            if(dis_sz[j] <= 0 || arr_ind[j] >= N) continue;
            ll tmp_profile = self_profile + arr[j][arr_ind[j]].first.val;
            mixco_cache[j][arr[j][arr_ind[j]++].second] = true;
            dis_sz[j]--;
            tmp_profile += get_distributed_profit();
            if(tmp_profile > mx_profile) {
                mx_ind = j;
                mx_profile = tmp_profile;
            }
            mixco_cache[j][arr[j][--arr_ind[j]].second] = false;
            dis_sz[j]++;
        }
        if(mx_profile <= res_profile) break;
        res_profile = mx_profile;
        self_profile += arr[mx_ind][arr_ind[mx_ind]].first.val;
        mixco_cache[mx_ind][arr[mx_ind][arr_ind[mx_ind]++].second] = true;
        dis_sz[mx_ind]--;
    }
    mixco = false;
    save_cache_to_file(3);
    return res_profile;
}
