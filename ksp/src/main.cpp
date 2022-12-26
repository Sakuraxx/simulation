#include "../include/ksp.h"
#include "../include/data.h"
#include "../include/util.h"
#include "../include/others.h"
#include <unistd.h>

void init_payment() {
    ori_payment = tot_req = 0;
    for(int ind = 0; ind < N; ind++) {
        for(int j = 0; j < M; j++) {
            tot_req += dn[ind][j];
            ori_payment += 1LL * global_cost[ind];  // 处理时延无法省略
        }
    }
}

double cal_rate(ll res, string mode) {
    double ori_delay = (double)ori_payment / tot_req;
    double after_delay = ((double)ori_payment - res) / tot_req;
    printf("%s: %.2lf ms, Rate: %.2lf%%\n", mode.c_str(), after_delay, 100.0 - after_delay / ori_delay * 100);
    return after_delay;
}

vector<double> res;
vector<double> pa;
void add_data() {
    pa.push_back(N);
    pa.push_back(M);
    pa.push_back(K);
    pa.push_back(ZIPF_range);
    pa.push_back(ZIPF_alpha);
    pa.push_back((double)ori_payment / tot_req);
    printf("\nN: %d, M: %d, K: %d\n", N, M, K);
    printf("Total Request: %lld\nBefore Delay: %lld ms\nAvg Delay: %.2f ms\n", tot_req, ori_payment, (double)ori_payment / tot_req);

    res.push_back(cal_rate(fsp(), "KSP"));
    res.push_back(cal_rate(get_self_top_profit(), "Self Top"));
    res.push_back(cal_rate(get_distributed_profit(), "Distributed"));
    res.push_back(cal_rate(get_mixco_profit(), "Mixco"));
}

clock_t t1 = clock();
void test_speed() {
    pa.push_back(N);
    pa.push_back(M);
    pa.push_back(K);
    pa.push_back(ZIPF_range);
    pa.push_back(ZIPF_alpha);
    pa.push_back((double)ori_payment / tot_req);
    // printf("\nN: %d, M: %d, K: %d\n", N, M, K);
    // printf("Total Request: %lld\nBefore Delay: %lld ms\nAvg Delay: %.2f ms\n", tot_req, ori_payment, (double)ori_payment / tot_req);

    t1 = clock();
    // res.push_back(cal_rate(fsp(), "KSP"));
    // res.push_back(cal_rate(get_self_top_profit(), "Self Top"));
    // printf("time ksp: %ld ms", clock() - t1);
    // t1 = clock();
    res.push_back(cal_rate(get_distributed_profit(), "Distributed"));
    printf("time distributed: %ld ms\n", clock() - t1);
    // res.push_back(cal_rate(get_mixco_profit(), "Mixco"));
}

int main() {
    // output_lp_file();
    // auto t1 = clock();
    // printf("KSP: %lld\n", fsp());
    // printf("KSP Time: %ld ms\n", clock() - t1);


    // // + MEC
    // for(int i = 0; i <= 0; i++) {
    //     K = 2000; M = 25;
    //     printf("\nM = %d\n", M);
    //     init_payment();
    //     t1 = clock();
    //     printf("KSP: %lld\n", fsp());
    //     printf("KSP Time: %ld ms\n", clock() - t1);
    // }

    // + K
    // for(int i = 0; i < 10; i++) {
    //     K = 1000 + 1000 * i;
    //     for(int j = 0; j < MAXM; j++) set_MEC_size(j);
    //     init_payment();
    //     printf("\nK = %d GB\n", K);
    //     t1 = clock();
    //     printf("KSP: %lld\n", fsp());
    //     printf("KSP Time: %ld ms\n", clock() - t1);

    //     // t1 = clock();
    //     // printf("Mixco: %lld\n", get_mixco_profit());
    //     // printf("Mixco Time: %ld ms\n", clock() - t1);
    // }

    // t1 = clock();
    // cal_rate(fsp(), "KSP");
    // printf("KSP Time: %ld ms\n", clock() - t1);

    // t1 = clock();
    // cal_rate(get_self_top_profit(), "Self Top");
    // printf("Self Top Time: %ld ms\n", clock() - t1);

    // t1 = clock();
    // cal_rate(get_distributed_profit(), "Distributed");
    // printf("Distributed Time: %ld ms\n", clock() - t1);

    // t1 = clock();
    // cal_rate(get_mixco_profit(), "Mixco");
    // printf("Mixco Time: %ld ms\n", clock() - t1);

    // 初始化 util.cpp 的随机值
    // N = 2e5, M = 25, K = 2000;

    int reqPerSecd = 1;
    period = 10; // 秒
    N = 100, M = 3, K = 1;
    ZIPF_alpha = 1.5; // 值越大每台MEC服务器上内容的流行度越相似，值越小每台MEC服务器上内容的流行度越不同
    ZIPF_range = reqPerSecd * period; // d[j][i] <= range
    freopen("in.cfg", "r", stdin);
    init_para(); // 设置tile大小、时延等参数
    init(); // 设置MEC存储大小、tile流行度、局部和全局收益

    // 以1sec为周期
    int T = 10;
    for(int i = 0; i < T; i++) {
        times = i;
        // 重新计算局部收益和全局收益
        recal_local_global_profit(1);
        printf("init() Time: %ld ms\n", clock() - t1);
        init_payment();
        add_data();
    }

    // 测试速度
    // for(int i = 0; i <= 10; i++) {
    //     M = 5 + i * 2;
    //     init_payment();
    //     test_speed();
    // }

    // 内容大小
    // for(int i = 0; i < 10; i++) {
    //     N = 500 + i * 100; M = 5;
    //     init_payment();
    //     add_data();
    // }

    // // MEC 大小
    // for(int i = 0; i < 10; i++) {
    //     K = 50 + i * 100;
    //     for(int j = 0; j < MAXM; j++) set_MEC_size(j);
    //     init_payment();
    //     add_data();
    // }

    // 流行度取值
    // for(int i = 0; i < 20; i++) {
    //     ZIPF_alpha = 1 + i * 0.1;
    //     init();
    //     init_payment();
    //     add_data();
    // }

    // freopen("data.output", "w", stdout);
    // int ct = 0;
    // for(int i = 0; i < (int)pa.size(); i += 6) {
    //     printf("%.0lf %.0lf %.0lf %.0lf %.2lf %.6lf ", pa[i], pa[i + 1], pa[i + 2], pa[i + 3], pa[i + 4], pa[i + 5]);
    //     printf("%.6lf %.6lf %.6lf %.6lf ", res[ct], res[ct + 1], res[ct + 2], res[ct + 3]);
    //     ct += 4;
    // }

    return 0;
}