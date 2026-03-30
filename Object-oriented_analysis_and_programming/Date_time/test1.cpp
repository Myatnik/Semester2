#include <iostream>
#include "date_time.h"
using namespace std;

int main()
{
    Date_time a;
    Date_time b(4, 11, 2008);

    cout << "a = " << a << endl;
    cout << "input a: "; cin >> a;
    cout << "a = " << a << endl;
    cout << "b = " << b << endl;
    a += b;
    cout << "a+=b = " << a << endl;

    return 0;
}