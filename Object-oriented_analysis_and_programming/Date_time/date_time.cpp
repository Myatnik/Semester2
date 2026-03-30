#include "date_time.h"

int Date_time::To_Julian(const Date_time r)
{
	int a = (14 - r.month) / 12;
	int y = r.year + 4800 - a;
	int m = r.month + 12 * a - 3;

	int part1 = (153 * m + 2) / 5;
	int part2 = y / 4;
	int part3 = y / 100;
	int part4 = y / 400;

	int jdn = r.day + part1 + 365 * y + part2 - part3 + part4 - 32045;

	return jdn;
}

Date_time Date_time::From_Julian(int jdn)
{
	int a = jdn + 32044;
	int b = (4 * a + 3) / 146097;
	int part1c = (146097 * b) / 4;
	int c = a - part1c;
	int d = (4 * c + 3) / 1461;
	int part1e = (1461 * d) / 4;
	int e = c - part1e;
	int m = (5 * e + 2) / 153;

	int part1 = (153 * m + 2) / 5;
	int part2 = m / 10;

	int day = e - part1 + 1;
	int month = m + 3 - 12 * part2;
	int year = 100 * b + d - 4800 + part2;

	Date_time grig(day, month, year);

	return grig;
};
//construct
Date_time::Date_time()
{
	day = 3;
	month = 10;
	year = 2007;
}

Date_time::Date_time(int day_input, int month_input, int year_input)
{
	day = day_input;
	month = month_input;
	year = year_input;
}
//addition and extraction
Date_time& Date_time::operator += (const Date_time r)
{
	*this = From_Julian(To_Julian(*this) + To_Julian(r));
	return *this;
}

//in and out
istream& operator >>(istream& in, Date_time& r)
{
	in >> r.day >> r.month >> r.year;
	return in;
}

ostream& operator << (ostream& out, const Date_time& r)
{
	out << r.day << "." << r.month << "." << r.year;
	return out;
}