#include <math.h>
#include <algorithm>
#include <cstdio>
#include "date_time.h"
using namespace std;

double Date_time::To_Julian(Date_time r)
{
	int a = (14 - r.month) / 12;
	int y = r.year + 4800 - a;
	int m = r.month + 12 * a - 3;

	int part1 = (153 * m + 2) / 5;
	int part2 = y / 4;
	int part3 = y / 100;
	int part4 = y / 400;

	int jdn_date = r.day + part1 + 365 * y + part2 - part3 + part4 - 32045;

	double jdn_time = (r.hour * 3600.0 + r.minute * 60.0 + r.second) / 86400.0;

	double jdn = jdn_date + jdn_time - 0.5;

	//cout << r << " " << jdn << endl; //for testing
	return jdn;
}

Date_time Date_time::From_Julian(double jdn)
{
	double jdn_corrected = jdn + 0.5;

	int jdn_date = (int)floor(jdn_corrected);
	double jdn_time = jdn_corrected - jdn_date;

	int total_seconds = (int)round(jdn_time * 86400.0);

	int hour = total_seconds / 3600;
	int minute = (total_seconds % 3600) / 60;
	int second = total_seconds % 60;

	int a = jdn_date + 32044;
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

	grig.hour = hour;
	grig.minute = minute;
	grig.second = second;
	grig.out_format = 0;
	grig.out_time = 0;

	return grig;
};

string Date_time::Format_number(int num)
{
	num = num % 100;
	return string(1, (num / 10) + '0') +
		string(1, (num % 10) + '0');
}

bool Date_time::Check_input(int second, int minute, int hour, int day, int month, int year)
{	
	static int days_per_month1[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
	static int days_per_month2[12] = {31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
	if (month < 1 or month > 12 or 
		day < 1 or
		hour < 0 or hour > 23 or
		minute < 0 or minute > 59 or
		second < 0 or second > 59)
		return false;
	if (day > days_per_month1[month-1] and (year % 4 != 0 or (year % 100 == 0 and year % 400 != 0)))
		return false;
	if (day > days_per_month2[month-1])
		return false;
	return true;
}

//construct
Date_time::Date_time()
{
	second = 0;
	minute = 0;
	hour = 0;
	day = 3;
	month = 10;
	year = 2007;
	out_format = 0;
	out_time = 0;
}

Date_time::Date_time(int day_input, int month_input, int year_input)
{
	if (Date_time::Check_input(0, 0, 0, day_input, month_input, year_input))
	{
		second = 0;
		minute = 0;
		hour = 0;
		day = day_input;
		month = month_input;
		year = year_input;
		out_format = 0;
		out_time = 0;
	}
	else
		throw Date_timeException();
}

Date_time::Date_time(const char* input)
{
	int second_input, minute_input, hour_input, day_input, month_input, year_input;

	int result = sscanf_s(input, "%4d-%2d-%2dT%2d:%2d:%2d",
		&year_input, &month_input, &day_input, &hour_input, &minute_input, &second_input);

	if (result == 6)
	{
		if (Date_time::Check_input(second_input, minute_input, hour_input, day_input, month_input, year_input))
		{
			second = second_input;
			minute = minute_input;
			hour = hour_input;
			day = day_input;
			month = month_input;
			year = year_input;
			out_format = 0;
			out_time = 1;
		}
		else
			throw Date_timeException();
	}
	else
		throw Date_timeException();
	
	
}
;
//addition and extraction
/*
Date_time& Date_time::operator += (const Date_time& r)
{
	*this = From_Julian(To_Julian(*this) + To_Julian(r));
	return *this;
}

Date_time Date_time::operator + (const Date_time &r) const
{
	Date_time res(*this);
	return res += r;
}

Date_time Date_time::operator - () const
{
	
}

Date_time Date_time::operator - (const Date_time&r) const
{
	
}

Date_time& Date_time::operator -= (const Date_time& r)
{
	
}*/

//special
int Date_time::Day_diff(const Date_time r, const Date_time m)
{
	int diff = max(To_Julian(r), To_Julian(m)) - min(To_Julian(r), To_Julian(m));

	return diff;
}

char* Date_time::Week_day(const Date_time r)
{
	static char days[] = "Mon\0Tue\0Wed\0Thu\0Fri\0Sat\0Sun\0";
	char* days_ptr = days;

	int day = To_Julian(r);
	int week_day = day % 7;
	days_ptr += week_day * 4;

	return days_ptr;
}

Date_time Date_time::Easter(const int year)
{
	int a = year % 19;
	int b = year % 4;
	int c = year % 7;
	int d = (19 * a + 15) % 30;
	int e = (2 * b + 4 * c + 6 * d + 6) % 7;
	int f = d + e;
	if (f <= 26)
		return Date_time(4 + f, 4, year);
	else
		return Date_time(f - 26, 5, year);
}

void Date_time::Change_out_format(Date_time& r)
{
	r.out_format++;
	r.out_format = r.out_format % 3;
}

void Date_time::Change_out_time(Date_time& r)
{
	r.out_time++;
	r.out_time = r.out_time % 2;
}

//in and out
istream& operator >>(istream& in, Date_time& r)
{	
	in >> r.day >> r.month >> r.year;
	if (Date_time::Check_input(r.second, r.minute, r.hour, r.day, r.month, r.year))
	{
		return in;
	}
	else
		throw Date_timeException();
}

ostream& operator << (ostream& out, const Date_time& r)
{
	if (r.out_format == 0)
		out << r.day << "." << Date_time::Format_number(r.month) << "." << r.year;
	if (r.out_format == 1)
	{
		static char months[] = "Jan\0Feb\0Mar\0Apr\0May\0Jun\0Jul\0Aug\0Sep\0Oct\0Nov\0Dec\0";
		char* months_ptr = months;

		months_ptr += (r.month - 1) * 4;

		out << r.day << " " << months_ptr << " " << r.year;
	}
	if (r.out_format == 2)
		out << Date_time::Format_number(r.day) << "." << Date_time::Format_number(r.month) << "." << Date_time::Format_number(r.year);
	if (r.out_time == 1)
		out << "," << Date_time::Format_number(r.hour) << ":" << Date_time::Format_number(r.minute) << ":" << Date_time::Format_number(r.second);
	return out;
}