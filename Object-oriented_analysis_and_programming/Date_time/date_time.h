#include <iostream>
using namespace std;
#pragma once

class Date_timeException{};
class Date_time
{
private:
	static double To_Julian(Date_time r);
	Date_time From_Julian(double jdn);
	static string Format_number(int num);
	static bool Check_input(int second, int minute, int hour, int day, int month, int year);
public:
	int second;
	int minute;
	int hour;
	int day;
	int month;
	int year;
	int out_format;
	int out_time;

	Date_time();
	Date_time(int day_input, int month_input, int year_input);
	Date_time(const char* input);
	/*
	Date_time& operator += (const Date_time& r);
	Date_time operator + (const Date_time& r) const;
	Date_time operator - () const;
	Date_time operator - (const Date_time& r) const;
	Date_time& operator -= (const Date_time& r);*/

	static int Day_diff(const Date_time r, const Date_time m);
	static char* Week_day(const Date_time r);
	static Date_time Easter(const int year);
	static void Change_out_format(Date_time& r);
	static void Change_out_time(Date_time& r);

	friend istream& operator >>(istream& in, Date_time& r);
	friend ostream& operator <<(ostream& out, const Date_time& r);

};
