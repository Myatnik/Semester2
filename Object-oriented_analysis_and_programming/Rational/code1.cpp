#include <iostream>
#include "rational.h"
using namespace std;

int main()
{
    cout << "Enter a b c for your quadratic equasion (ax**2 + bx + c = 0)" << endl;
    Rational a, b, c;
    cout << "Enter a: "; cin >> a;
    cout << "Enter b: "; cin >> b;
    cout << "Enter c: "; cin >> c;
    cout << "Your equasion is " << a << "x**2 + " << b << "x + " << c << " = 0" << endl;

    Rational zero;
    Rational discr = b * b - Rational(4) * a * c;
    if (discr < zero)
    {
        cout << "Discr is " << discr << " < 0, no solutions" << endl;
        return 1;
    }
    Rational answ_den = Rational(2) * a;
    Rational answ_root = discr.sqr_root();

    Rational x1, x2;
    x1 = (-b + answ_root) / answ_den;
    x2 = (-b - answ_root) / answ_den;
    
    cout << "Your answers are " << x1 << " and " << x2;

    return 0;
}