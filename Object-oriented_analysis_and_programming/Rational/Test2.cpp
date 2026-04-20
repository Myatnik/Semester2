#include <iostream>
#include "rational.h"
using namespace std;

int main()
{
    Rational a, b(3), c(4, 6);
    cout << a << endl;
    cin >> a;
    cout << "a = " << a << endl;
    cout << "b = " << b << endl;
    cout << "c = " << c << endl;
    cout << "---" << endl;

    /*
    cout << a + b << endl;*/ //use to test exceptions, a = 2147483647/1

    /*
    cout << b + c << endl;
    b += c;
    cout << b << endl;
    b -= c;
    cout << b << endl;
    cout << b-- << endl;
    cout << b << endl;*/

    /*
    if (b == a) {
        cout << "equal" << endl;
    }
    if (b != a) {
        cout << "not equal" << endl;
    }
    if (b < a) {
        cout << "less" << endl;
    }
    if (b <= a) {
        cout << "not more" << endl;
    }
    if (b > a) {
        cout << "more" << endl;
    }
    if (b >= a) {
        cout << "not less" << endl;
    }*/

    /*
    cout << a * b << endl;
    Rational d(2, 3);
    cout << d << endl;
    d *= a;
    cout << d << endl;
    cout << b / a << endl;*/

    /*
    cout << int(a) << endl;
    cout << double(a) << endl;*/

    return 0;
}