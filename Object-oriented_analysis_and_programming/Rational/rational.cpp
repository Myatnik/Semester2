#include <math.h>
#include "rational.h"
using namespace std;
//simplify
void Rational::simplify() {
	if (denom < 0)
	{
		numer = -numer;
		denom = -denom;
	}
	
	int numer_save = abs(numer);
	int denom_save = abs(denom);
	while (numer_save != 0 and denom_save != 0)
	{
		if (numer_save > denom_save)
			numer_save = numer_save % denom_save;
		else
			denom_save = denom_save % numer_save;
	}
	int nod = numer_save + denom_save;
	numer = numer / nod;
	denom = denom / nod;
}
//construct
Rational::Rational()
{
	numer = 0;
	denom = 1;
}

Rational::Rational(int number_input)
{
	numer = number_input;
	denom = 1;
}

Rational::Rational(int number_input, int denom_input)
{
	numer = number_input;
	denom = denom_input;
	simplify();
}
//addition and extraction
Rational& Rational::operator += (const Rational r) //did a throw exception
{
	if ((denom > INT_MAX / r.denom) or 
		(numer > 0 and numer > INT_MAX / r.denom) or 
		(numer < 0 and numer < INT_MIN / r.denom) or 
		(r.numer > 0 and r.numer > INT_MAX / denom) or 
		(r.numer < 0 and r.numer < INT_MIN / denom) or
		(denom * r.numer > 0 and numer * r.denom > INT_MAX - denom * r.numer) or
		(denom * r.numer < 0 and numer * r.denom < INT_MIN - denom * r.numer))
	{
		throw RationalException();
	}
	else {
		numer = (numer * r.denom + denom * r.numer);
		denom *= r.denom;
		simplify();
		return *this;
	}
} 

Rational Rational::operator + (const Rational &r) const
{
	Rational res(*this);
	return res += r;
}

Rational Rational::operator - () const
{
	Rational r(-numer, denom);
	return r;
}

Rational Rational::operator - (const Rational &r) const
{
	Rational res(*this);
	return res -= r;
}

Rational& Rational::operator -= (const Rational& r)
{
	return (*this += (-r));
}
//multiplication and division
Rational& Rational::operator *= (const Rational& r)
{
	if ((numer > 0 and r.numer > 0 and numer > INT_MAX / r.numer) or
		(numer > 0 and r.numer < 0 and r.numer < INT_MIN / numer) or
		(numer < 0 and r.numer > 0 and numer < INT_MIN / r.numer) or
		(numer < 0 and r.numer < 0 and r.numer < INT_MAX / numer))
	{
		throw RationalException();
	}
	else {
		numer = numer * r.numer;
		denom = denom * r.denom;
		simplify();
		return *this;
	}
}

Rational Rational::operator * (const Rational& r) const
{
	Rational res(numer, denom);
	return (res *= r);
}

Rational& Rational::operator /= (const Rational& r)
{
	Rational divider(r.denom, r.numer);
	return(*this *= divider);
}

Rational Rational::operator / (const Rational& r) const
{
	Rational res(numer, denom);
	return res /= r;
}
//increment and decrement
Rational& Rational::operator ++()
{
	numer += denom;
	return *this;
}

Rational Rational::operator ++(int)
{
	Rational r(*this);
	numer += denom;
	return r;
}

Rational& Rational::operator --()
{
	numer -= denom;
	return *this;
}

Rational Rational::operator --(int)
{
	Rational r(*this);
	numer -= denom;
	return r;
}
//logical operators
bool Rational::operator ==(const Rational& r) const
{
	return (numer == r.numer) && (denom == r.denom);
}

bool Rational::operator !=(const Rational& r) const
{
	return !(*this == r);
}

bool Rational::operator >(const Rational& r)const
{
	return int(*this) > int(r);
}

bool Rational::operator >=(const Rational& r)const
{
	return int(*this) >= int(r);
}

bool Rational::operator <(const Rational& r)const
{
	return !(*this >= r);
}

bool Rational::operator <=(const Rational& r)const
{
	return !(*this > r);
}
//into other types
Rational::operator int() const
{
	return numer / denom;
}

Rational::operator double() const
{
	return ((double)numer) / denom;
}
//in and out
istream& operator >>(istream& in, Rational& r)
{
	in >> r.numer >> r.denom;
	r.simplify();
	return in;
}

ostream& operator << (ostream& out, const Rational& r)
{
	out << r.numer << "/" << r.denom;
	return out;
}