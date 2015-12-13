// __Filename__ - __CF_Contest__ by __User__ __Year__

#include <bits/stdc++.h>
using namespace std;

// CPlusPlusUnit - C++ Unit testing TDD framework (github.com/cppunit/cppunit)
class Cppunit { public:
    #define CHECK(a,b)  check<long long>(a, b, #a, #b, __FILE__, __LINE__, __FUNCTION__);
    #define CHECKT(a)   check<bool>(a, true, #a, "true", __FILE__, __LINE__, __FUNCTION__);
    #define CHECKS(a,b) check<cs>(a, b, #a, #b, __FILE__, __LINE__, __FUNCTION__);
    typedef const std::string& cs;
    int checks, fails; std::ostringstream serr; std::istringstream *in;
    Cppunit() { checks = fails = 0;}
    void test_cin(cs s){ in = new std::istringstream(s); std::cin.rdbuf(in->rdbuf()); }
    void fail_hdr(cs stra, cs strb, cs file, int line, cs func) {
        serr << "==================================================" << std::endl;
        serr << "FAIL: " << func << std::endl;
        serr << "--------------------------------------------------" << std::endl;
        serr << "File \"" << file << "\", line " << line << " in " << func << std::endl;
        serr << "  Checking " << stra << " == " << strb << std::endl;
    }
    template <typename T> void check(T a, T b, cs stra, cs strb, cs file, int line, cs func) {
        checks++; if (a == b) { std::cout << "."; return; }
        fails++; std::cout << "F"; fail_hdr(stra, strb, file, line, func);
        serr << "  Error: \"" << a << "\" ! = \"" << b << "\"" << std::endl << std::endl;
    }
    virtual void single_test() {}
    virtual void test_list() { single_test(); }
    double dclock() { return double(clock()) / CLOCKS_PER_SEC; }
    int status() {
        std::cout << std::endl; if (fails) std::cout << serr.str();
        std::cout << "--------------------------------------------------" << std::endl;
        std::cout << "Ran " << checks << " checks in " << dclock() << "s" << std::endl << std::endl;
        if (fails) std::cout << "FAILED (failures=" << fails << ")"; else std::cout << "OK" << std::endl;
        return fails > 0;
    }
    int run() { std::streambuf* ocin = std::cin.rdbuf(); test_list(); std::cin.rdbuf(ocin); return status(); }
};

///////////////////////////////////////////////////////////////////////////////
// __Class__ Class (Main Program)
///////////////////////////////////////////////////////////////////////////////


class __Class__ { public:

    typedef long long ll;
    ll n, m;
    vector <ll> numa, numb, nums;

    __Class__(){

        // Reading single elements
        cin >> n;
        cin >> m;

        // Reading multiple lines of pair
        for(int i=0; i<n; i++) {
            ll a; cin >> a; numa.push_back(a);
            ll b; cin >> b; numb.push_back(b);
        }

        // Reading a single line of multiple elements
        for(int i=0; i<m; i++) {
            ll s; cin >> s; nums.push_back(s);
        }
    }

    string calculate(){

        // Result calculation
        ll result = 0;

        // Converting result to string
        ostringstream resstr;
        resstr << result;
        return resstr.str();
    }
};

///////////////////////////////////////////////////////////////////////////////
// Unit tests
///////////////////////////////////////////////////////////////////////////////


class MyCppunit: public Cppunit {

    __Class__* d;

    void single_test() {

        // Constructor test
        string test = "2 3\n1 2\n3 4\n1 2 3 4";
        test_cin(test);
        d = new __Class__;
        CHECK(d->n, 2);
        CHECK(d->m, 3);
        CHECK(d->numa[0], 1);
        CHECK(d->numb[0], 2);
        CHECK(d->nums[0], 1);

        // Sample test
        test_cin(test);
        //CHECKS((new __Class__)->calculate(), "0");

        // Sample test
        test_cin("");
        //CHECKS((new __Class__)->calculate(), "0");

        // Sample test
        test_cin("");
        //CHECKS((new __Class__)->calculate(), "0");

        // My test
        test_cin("");
        //CHECKS((new __Class__)->calculate(), "0");

        // Time limit test
        //time_limit_test(2000);
    }

    void time_limit_test(int nmax){

        int mmax = nmax;
        ostringstream stest;

        // Random inputs
        stest << nmax << " " << mmax << endl;
        for(int i = 0; i < nmax; i++) stest << i << " " << i+1 << endl;
        for(int i = 0; i < mmax; i++) stest << rand() % 40 << " ";

        // Run the test
        double start = dclock();
        test_cin(stest.str());
        d = new __Class__;
        double calc = dclock();
        d->calculate();
        double stop = dclock();
        cout << endl << "Timelimit Test: " << stop - start << "s (init ";
        cout << calc - start << "s calc " << stop - calc << "s)" << endl;
    }
};


int main(int argc, char *argv[]) {

    // Faster cin and cout
    ios_base::sync_with_stdio(0);cin.tie(0);

    if (argc > 1 && !strcmp(argv[1], "-ut"))
        return (new MyCppunit)->run();

    cout << (new __Class__)->calculate();
    return 0;
}

