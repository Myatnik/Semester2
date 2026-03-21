#include <iostream>
#include <fstream>
#include <chrono>
#include "array.h"
using namespace std;

int main()
{
    cout << "Input amount of numbers and step (N, s)" << endl;
    int N, s;
    cout << "Input N: "; cin >> N;
    cout << "Input s: "; cin >> s;

    Array nums(N);
    for (int i = 0; i < N;i++)
    {
        nums.insert(i+1, i);
    }

    int nums_left = N;
    int current_erase = s;

    auto start = chrono::steady_clock::now(); //time count begins

    while (nums_left != 1) //only main loop counts into working time
    {
        nums.remove(current_erase-1);
        nums_left--;
        current_erase += s-1;
        if (current_erase > nums_left)
        {
            current_erase -= nums_left;
        }
    }
    
    auto end = chrono::steady_clock::now(); //time count ends

    cout << "Last number standing is " << nums[0] << endl;

    chrono::duration<double> duration = end - start;
    int diff = static_cast<int>(duration.count());


    cout << "Work time: " << diff << " sec" << endl;
    
    ofstream file("Results.csv", ios::app);
    file << N << "," << diff << "\n";
    file.close();

    return 0;
}