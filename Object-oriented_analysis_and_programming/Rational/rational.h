#include <iostream>
using namespace std;
#pragma once

class RationalException{};
class Rational
{
private:
	void simplify();
public:
	int numer;
	int denom;

	Rational();
	Rational(int number_input);
	Rational(int number_input, int denom_input);

	Rational& operator += (const Rational r);
	Rational operator + (const Rational& r) const;
	Rational operator - () const;
	Rational operator - (const Rational& r) const;
	Rational& operator -= (const Rational& r);

	Rational& operator *= (const Rational& r);
	Rational operator * (const Rational& r) const;
	Rational& operator /= (const Rational& r);
	Rational operator / (const Rational& r) const;

	Rational& operator ++();
	Rational operator ++(int);
	Rational& operator --();
	Rational operator --(int);

	bool operator ==(const Rational& r) const;
	bool operator !=(const Rational& r) const;
	bool operator >(const Rational& r) const;
	bool operator >=(const Rational& r) const;
	bool operator <(const Rational& r) const;
	bool operator <=(const Rational& r) const;

	operator int() const; 
	operator double() const;

	friend istream& operator >>(istream& in, Rational& r); 
	friend ostream& operator <<(ostream& out, const Rational& r);
};
