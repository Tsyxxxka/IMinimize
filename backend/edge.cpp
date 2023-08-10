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

    
    string outName = "./edges-" + fileName;
    cout << outName << endl;
    fileName = "./" + fileName;
    ifstream in(fileName.c_str());
    ofstream out(outName.c_str());

    int n, m;
    in >> n >> m;
    out<<n<<" "<<m<<endl;
    vector<PII> E;
    vector<int> inDegree;
    inDegree.resize(n);
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
            out<<x<<" "<<y<<" "<<p<<endl;
        }
    }
    double endTime = clock();
    cout << "Finish loading dataset. time : " << (endTime - beginTime) / CLOCKS_PER_SEC << "s." << endl;
    return 0;
}