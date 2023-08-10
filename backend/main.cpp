
#include <bits/stdc++.h>
using namespace std;
#define LL long long
#define LD long double
#define PII pair<int, int>

struct Edge
{
    int to;
    double p;
    Edge(int a = 0, double b = 0) : to(a), p(b) {}
};
mt19937 rand_num(20220708);

double randEdge()
{
    uniform_int_distribution<int> dist(1, 3);
    int x = dist(rand_num);
    if (x == 1)
        return 0.1;
    else if (x == 2)
        return 0.01;
    return 0.001;
}

bool check(int x)
{
    uniform_int_distribution<int> dist(1, x);
    if (dist(rand_num) == 1)
        return true;
    return false;
}

struct tl
{
    int clk;
    vector<int> fa, idx, ridx, c, best, semi, idom, sum;
    vector<vector<int>> dt, G, rG;
    void init(int n, vector<vector<int>> e)
    {
        G.clear();
        G = e;
        fa.clear();
        fa.resize(n + 1);
        idx.clear();
        idx.resize(n + 1);
        ridx.clear();
        ridx.resize(n + 1);
        c.clear();
        c.resize(n + 1);
        best.clear();
        best.resize(n + 1);
        dt.clear();
        dt.resize(n + 1);
        rG.clear();
        rG.resize(n + 1);
        semi.clear();
        semi.resize(n + 1);
        idom.clear();
        idom.resize(n + 1);
        sum.clear();
        sum.resize(n + 1);
        clk = 0;
        for (int i = 0; i <= n; i++)
        {
            sum[i] = 0;
            c[i] = -1;
            semi[i] = i;
            best[i] = i;
            idx[i] = 0;
            for (int v : G[i])
                rG[v].push_back(i);
        }
    }
    void dfs(int u)
    {
        idx[u] = ++clk;
        ridx[clk] = u;
        for (int &v : G[u])
            if (!idx[v])
            {
                fa[v] = u;
                dfs(v);
            }
    }
    int fix(int x)
    {
        if (c[x] == -1)
            return x;
        int &f = c[x], rt = fix(f);
        if (idx[semi[best[x]]] > idx[semi[best[f]]])
            best[x] = best[f];
        return f = rt;
    }
    void compute(int x)
    {
        sum[x] = 1;
        for (auto y : dt[x])
        {
            compute(y);
            sum[x] += sum[y];
        }
    }
    void go(int rt)
    {
        dfs(rt);
        for (int i = clk; i > 1; i--)
        {
            int x = ridx[i], mn = clk + 1;
            for (int &u : rG[x])
            {
                if (!idx[u])
                    continue;
                fix(u);
                mn = min(mn, idx[semi[best[u]]]);
            }
            c[x] = fa[x];
            dt[semi[x] = ridx[mn]].push_back(x);
            x = ridx[i - 1];
            for (int &u : dt[x])
            {
                fix(u);
                if (semi[best[u]] != x)
                    idom[u] = best[u];
                else
                    idom[u] = x;
            }
            dt[x].clear();
        }
        for (int i = 2; i <= clk; i++)
        {
            int u = ridx[i];
            if (idom[u] != semi[u])
                idom[u] = idom[idom[u]];
            dt[idom[u]].push_back(u);
            // cout<<idom[u]<<" "<<u<<endl;
        }
        compute(rt);
    }
} tree;

vector<int> vis_num;

double compute_expected(int T, int n, vector<vector<Edge>> e, vector<int> sources)
{
    vector<int> vis;
    vis.resize(n);
    double beginTime = clock(), endTime;
    double sum = 0;
    for (int tag = 1; tag <= T; tag++)
    {
        vector<vector<Edge>> eSample;
        eSample.resize(n);
        queue<int> q;
        for (auto x : sources)
            q.push(x), vis[x] = -tag;
        while (!q.empty())
        {
            int x = q.front();
            q.pop();
            for (auto y : e[x])
            {
                if (y.p == 0)
                    continue;
                if (check((int)round(1.0 / y.p)))
                {
                    eSample[x].push_back(y.to);
                    if (vis[y.to] != -tag)
                        q.push(y.to), vis[y.to] = -tag;
                }
            }
        }
        for (auto x : sources)
            vis[x] = tag, sum += 1.0, q.push(x);
        while (!q.empty())
        {
            int x = q.front();
            vis_num[x]++;
            q.pop();
            for (auto y : eSample[x])
                if (vis[y.to] != tag)
                    vis[y.to] = tag, sum += 1.0, q.push(y.to);
        }
    }
    endTime = clock();
    return sum / ((double)T);
}

void compute_block(int n, vector<vector<int>> e, vector<int> sources, vector<double> &sum)
{
    e.push_back(sources);
    tree.init(n, e);

    tree.go(n);
    for (int i = 0; i < n; i++)
        sum[i] += (double)tree.sum[i];
}

void compute_candidate(int &remove_node, int n, vector<vector<Edge>> e, vector<int> sources, vector<int> remove_flag)
{
    int T = 10000;
    vector<int> vis;
    vector<double> sum;
    double beginTime = clock(), endTime;
    for (int i = 0; i < n; i++)
        vis.push_back(0), sum.push_back(0);
    for (int tag = 1; tag <= T; tag++)
    {
        vector<vector<int>> eSample;
        eSample.resize(n);
        queue<int> q;
        for (auto x : sources)
            q.push(x), vis[x] = -tag;
        while (!q.empty())
        {
            int x = q.front();
            q.pop();
            for (auto y : e[x])
            {
                if (y.p == 0)
                    continue;
                if (check((int)round(1.0 / y.p)))
                {
                    eSample[x].push_back(y.to);
                    if (vis[y.to] != -tag)
                        q.push(y.to), vis[y.to] = -tag;
                }
            }
        }
        compute_block(n, eSample, sources, sum);
    }
    endTime = clock();

    double Max = -1;
    for (int i = 0; i < n; i++)
        if (!remove_flag[i])
            if (sum[i] / ((double)T) > Max)
                Max = sum[i] / ((double)T), remove_node = i;
}

int main()
{
    cout << "dataset: ";
    string fileName;
    cin >> fileName;
    double beginTime = clock();

    cout << "propagation model (0: TR model; 1: WC model; 2: Customize): ";
    int model;
    cin >> model;

    cout << "number of seeds : ";
    int num_source, x;
    cin >> num_source;

    vector<int> sources;
    cout << "seeds : ";
    for (int i = 0; i < num_source; i++)
        cin >> x, sources.push_back(x);

    cout << "budget: ";
    int budget;
    cin >> budget;
    string outName = "./results-" + fileName;
    cout << outName << endl;
    fileName = "./" + fileName;
    ifstream in(fileName.c_str());
    ofstream out(outName.c_str());

    int n, m;
    in >> n >> m;

    vector<PII> E;
    vector<int> inDegree;
    inDegree.resize(n);
    vis_num.resize(n);
    vector<vector<Edge>> e;
    e.resize(n);
    for (int i = 0; i < m; i++)
    {
        if (model == 2)
        {
            int x, y;
            double z;
            in >> x >> y >> z;
            E.push_back(PII(x, y));
            inDegree[y]++;
            e[x].push_back(Edge(y, z));
        }
        else
        {
            int x, y;
            in >> x >> y;
            E.push_back(PII(x, y));
            inDegree[y]++;
        }
    }

    if (model < 2)
    {
        for (auto edge : E)
        {
            int x = edge.first, y = edge.second;
            double p;
            if (model == 0)
                p = randEdge();
            else
                p = 1.0 / ((double)inDegree[y]);
            e[x].push_back(Edge(y, p));
        }
    }
    double endTime = clock();
    // cout << "Finish loading dataset. time : " << (endTime - beginTime) / CLOCKS_PER_SEC << "s." << endl;

    double res = compute_expected(10000, n, e, sources);
    out <<n <<"\t"<<res - ((double)num_source)<<"\t";

    vector<int> remove_flag;
    for (int i = 0; i < n; i++)
        remove_flag.push_back(0);
    for (auto x : sources)
        remove_flag[x] = 1;
    vector<int> blocker;
    double totalTime = 0;
    for (int B = 1; B <= budget; B++)
    {
        beginTime = clock();
        int remove_node;
        compute_candidate(remove_node, n, e, sources, remove_flag);

        remove_flag[remove_node] = 1;
        vector<vector<Edge>> e_tmp;
        e_tmp.resize(n);
        for (int u = 0; u < n; u++)
            if (u != remove_node)
            {
                for (auto v : e[u])
                    if (v.to != remove_node)
                        e_tmp[u].push_back(v);
            }
        remove_flag[remove_node] = 1;
        blocker.push_back(remove_node);
        e = e_tmp;
        endTime = clock();
        totalTime += endTime - beginTime;
    }

    for (int i=0;i<n;i++)
        vis_num[i] = 0;
    res = compute_expected(10000, n, e, sources);
    out << res- ((double)num_source) << endl;
    
    for (auto x:blocker)
        out<<x<<"\t";
    out<<endl;
    for (int i=0;i<n;i++)
    {
        double ap=((double)vis_num[i])/10000.0;
        if (ap>1) ap=1;
        out<<i<<"\t"<<ap<<endl;
    }

    return 0;
}