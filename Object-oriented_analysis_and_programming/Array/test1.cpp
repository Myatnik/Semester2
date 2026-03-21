#include <iostream>
#include "array.h"
using namespace std;

int main()
{
    Array test1(10);

    cout << test1 << endl;
    cout << test1.getSize() << endl;
    cout << "---" << endl;

    test1.insert(1);
    test1.insert(2);
    test1.insert(3, 1);
    cout << test1 << endl;
    test1.remove(0);
    cout << test1 << endl;
    cout << test1[0] << endl;

    return 0;
}