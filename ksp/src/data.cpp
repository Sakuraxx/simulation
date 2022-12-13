#include "../include/data.h"
#include "../include/util.h"

using namespace std;

// for saving cache file
int period;
int times;

int storages[MAXM];            // MEC 的存储能力
Node local_profit[MAXM][MAXN]; // 局部收益
Node global_profit[MAXN];      // 全局收益 (云端时延 * MEC 数量 * 到达量 dn = 300 * 10 * 1000 = 3e6)

int ZIPF_range = 10000;     // zipf 值域
double ZIPF_alpha = 2;    // zipf 集中度
int BLOCK_SIZE = 10;     // 数据块大小 (MByte)
int QUEUING_DELAY = 5;   // (ms) 排队时延
int PROCESS_DELAY = 5;   // (ms) 处理时延

int CLOUD_PROPAGATION_DELAY = 50;   // (ms) 云端传播时延
int MEC_BAND = 1000;     // (MBps) MEC 之间带宽
int USER_BAND = 100;     // (MBps) 用户带宽
int dn[MAXN][MAXM];
int N, M, K, seed_num;
ll ori_payment = 0;
ll tot_req = 0;

int global_cost[MAXN];

// 暂存流行度
int p_dn[MAXN][MAXM];
int f_dn[MAXN][MAXM];

void generate_tile_param(int ind) {
    // int dn_base = zipf(ZIPF_alpha, ZIPF_range);
    
    // 预取: 初始化 tile ind 在所有 mec 上的流行分布
    for(int j = 0; j < MAXM; j++) {
        // dn[ind][j] = dn_base + 10 * rand_val(0);
        
        // 0% ~ 10%
        // dn[ind][j] *= rand_val(0);
        dn[ind][j] = zipf(ZIPF_alpha, ZIPF_range);

        int fail_dn = rand_val(0) / 10 * dn[ind][j];
        int predict_dn = dn[ind][j] - fail_dn;

        f_dn[ind][j] = fail_dn;
        p_dn[ind][j] = predict_dn;

        // 50% ~ 60%
        int send_sz = BLOCK_SIZE * (rand_val(0) / 10 + 0.5);
        int c_mec_to_cloud = QUEUING_DELAY + 1000 * send_sz / MEC_BAND + 
                            CLOUD_PROPAGATION_DELAY + 100 * rand_val(0);  // MEC 到云端
        int c_mec_to_mec   = QUEUING_DELAY + 1000 * send_sz / MEC_BAND; // MEC 到 MEC
        int c_user_to_mec  = QUEUING_DELAY + 1000 * send_sz / USER_BAND; // 用户到 MEC
        
        // 预测时延
        local_profit[j][ind].val = predict_dn * c_mec_to_mec;
        global_profit[ind].val = predict_dn * (c_mec_to_cloud - c_mec_to_mec);
        global_cost[ind] = predict_dn * (c_user_to_mec + c_mec_to_cloud);

        // 10% ~ 20%
        send_sz = BLOCK_SIZE * (rand_val(0) / 10 + 0.1);
        c_mec_to_cloud = QUEUING_DELAY + 1000 * send_sz / MEC_BAND + 
                          CLOUD_PROPAGATION_DELAY + 100 * rand_val(0);  // MEC 到云端
        c_mec_to_mec   = QUEUING_DELAY + 1000 * send_sz / MEC_BAND; // MEC 到 MEC
        c_user_to_mec  = QUEUING_DELAY + 1000 * send_sz / USER_BAND; // 用户到 MEC

        local_profit[j][ind].val += fail_dn * c_mec_to_mec;
        global_profit[ind].val += fail_dn * (c_mec_to_cloud - c_mec_to_mec);
        global_cost[ind] += fail_dn * (c_user_to_mec + c_mec_to_cloud + PROCESS_DELAY);
    }
}

void set_MEC_size(int j) {
    int gb = K;
    storages[j] = gb * 1000 / BLOCK_SIZE;
    // printf("MEC[%d]  Space: %d GB  Ki: %d.\n", j, gb, storages[j]);
}

void init_para() {
    scanf("%d%d%d%d", &seed_num, &BLOCK_SIZE, &QUEUING_DELAY, &PROCESS_DELAY);
    scanf("%d%d%d", &CLOUD_PROPAGATION_DELAY, &MEC_BAND, &USER_BAND);
    srand(seed_num);
    rand_val(seed_num);
}

void init() {
    // 5379062 4399726
    // time_t tt = time(0);
    // cout << tt << endl;
    first = 1;
    for(int i = 0; i < MAXM; i++) set_MEC_size(i);
    for(int i = 0; i < MAXN; i++) generate_tile_param(i);

    // 记录下流量分布
    fstream dn_file;
    stringstream s;
    s << "../data/dn_" << period << "_" << times << ".txt";
    dn_file.open(s.str(), ios::out);  // write,清空再写入
    if (dn_file.is_open())
    {
        for(int i = 0; i < N; i++) {
            for(int j = 0; j < M; j++) {
                dn_file << j << " " << i << " " << p_dn[i][j] << " " << f_dn[i][j] << "\n"; // mid tid p_num f_num
            }
        }
    } else {
        printf("open failed.\n");
    }
    dn_file.close();
}

void output_lp_file() {
    FILE* fp = fopen("lp.input", "w");
    fprintf(fp, "Maximize\n");

    fprintf(fp, "obj: ");
    for(int n = 0; n < N; n++) {
        for(int m = 0; m < M; m++) {
            fprintf(fp, "%d f2%d%d + ", local_profit[m][n].val, n, m);
        }
        fprintf(fp, "%d f1s%d0 %c ", global_profit[n].val, n, N - 1 == n ? '\n' : '+');
    };

    fprintf(fp, "\nSubject To\n");
    int cnt = 1;

    string in_flows, out_flows;

    // 添加流守恒约束和流变量约束
    for(int n = 0; n < N; n++) {
        in_flows = "";
        for(int d = 0; d < M; d++) {
            in_flows += "f1s" + to_string(n) + to_string(d);
            if(d != M - 1) in_flows += " + ";
        }
        out_flows = "";
        for(int m = 0; m < M; m++) {
            out_flows += " - f2" + to_string(n) + to_string(m);
        }
        
        fprintf(fp, "\nc%d: %s\n%s = 0\n", cnt++, in_flows.c_str(), out_flows.c_str());
    }

    out_flows = "";
    for(int n = 0; n < N; n++) {
        for(int d = 0; d < M; d++) {
            out_flows += "f1s" + to_string(n) + to_string(d);
            if(d != M - 1) out_flows += " + ";
        }
    }
    in_flows = "";
    for(int m = 0; m < M; m++) {
        for(int d = 0; d < K * 100; d++) {
            in_flows += " - f3" + to_string(m) + "t" + to_string(d);
        }
    }
    fprintf(fp, "\nc%d: %s\n%s = 0\n", cnt++, out_flows.c_str(), in_flows.c_str());
    
    for(int m = 0; m < M; m++) {
        in_flows = "";
        for(int n = 0; n < N; n++) {
            in_flows += "f2" + to_string(n) + to_string(m);
            if(n != N - 1) in_flows += " + ";
        }
        out_flows = "";
        for(int d = 0; d < K * 100; d++) {
            in_flows += " - f3" + to_string(m) + "t" + to_string(d);
        }
        fprintf(fp, "\nc%d: %s\n%s = 0\n", cnt++, out_flows.c_str(), in_flows.c_str());
    }

    fprintf(fp, "\nBounds\n");

    for(int n = 0; n < N; n++) {
        for(int d = 0; d < M; d++) {
            fprintf(fp, "\n0 <= f1s%d%d <= 1\n", n, d);
        }
        for(int m = 0; m < M; m++) {
            fprintf(fp, "\n0 <= f2%d%d <= 1\n", n, m);
        }
    }

    for(int m = 0; m < M; m++) {
         for(int d = 0; d < K * 100; d++) {
            fprintf(fp, "\n0 <= f3%dt%d <= 1\n", m, d);
         }
    }

    fprintf(fp, "End\n");

    fclose(fp);
}