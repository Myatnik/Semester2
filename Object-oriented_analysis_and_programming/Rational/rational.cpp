#include <math.h>
#include "rational.h"
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
Rational& Rational::operator += (const Rational r)
{
	numer = (numer*r.denom + denom*r.numer);
	denom *= r.denom;
	simplify();
	return *this;
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
	numer = numer * r.numer;
	denom = denom * r.denom;
	simplify();
	return (*this);
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
//root
Rational Rational::sqr_root() const
{
	if (numer == 0) {
		Rational Xn;
		return Xn;
	}
	int numer1 = numer;
	int denom1 = denom;

	for (int j = 0; j < 3; j++)
	{
		denom1 = (denom1 + denom / denom1) / 2;
	}
	for (int j = 0; j < 3; j++)
	{
		numer1 = (numer1 + numer / numer1) / 2;
	}
	Rational Xn(numer1, denom1);
	return Xn;
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