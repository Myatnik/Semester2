#include <iostream>
#include "date_time.h"
using namespace std;

int main()
{
    Date_time a;
    Date_time b(4, 2, 2008);
    Date_time c("2024-12-25T14:30:45");

    cout << "---basic math---" << endl;
    cout << "a = " << a << endl;
    cout << "input a: "; cin >> a;
    cout << "a = " << a << endl;
    cout << "b = " << b << endl;
    cout << "c = " << c << endl;

    cout << "---special functions---" << endl;
    cout << "Difference between a and b is " << Date_time::Day_diff(a, b) << " days" << endl;
    cout << "a is " << Date_time::Week_day(a) << endl;
    //int year; cout << "input year: "; cin >> year; cout << "Easter in " << year << " is at " << Date_time::Easter(year) << endl;
    cout << "Out format 1: " << a << endl; Date_time::Change_out_format(a);
    cout << "Out format 2: " << a << endl; Date_time::Change_out_format(a);
    cout << "Out format 3: " << a << endl; Date_time::Change_out_format(a);
    cout << "Out time format 1: " << a << endl; Date_time::Change_out_time(a);
    cout << "Out time format 2: " << a << endl; Date_time::Change_out_time(a);

    return 0;
}