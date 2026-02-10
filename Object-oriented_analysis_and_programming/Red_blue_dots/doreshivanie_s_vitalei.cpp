#include <iostream>
#include <random>
#include <time.h>
#include <math.h>
using namespace std;

int mn = 0;

void swap(int* M, int i1, int n) //переставляет элемент в конец массива и сдвигает все оставшиеся влево
{
    int save = M[i1];
    for (int i = 0; i < 2 * n - i1 - 1;i++)
    {
        M[i1 + i] = M[i1 + i + 1];
    }
    M[2 * n - 1] = save;
}
float leng(int x1, int y1, int x2, int y2) //считает расстояние между точками
{
    return sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2));
}
void f(int* XCords, int* YCords, int n)
{
    //for (int i = 0; i < n;)

}

int main()
{
    int seed = time(NULL);
    srand(seed);

    int n;
    cout << "Enter n";
    cin >> n;

    int* XCords = new int[2 * n]; // R1, R2 ... Rn, B1...
    for (int i = 0; i < 2 * n; i++) {
        XCords[i] = rand() % 21 - 10;
        cout << XCords[i] << " ";
    }
    cout << endl;

    int* YCords = new int[2 * n];
    for (int i = 0; i < 2 * n; i++) {
        YCords[i] = rand() % 21 - 10;
        cout << YCords[i] << " ";
    }
    cout << endl;


    delete[] XCords;
    delete[] YCords;

    return 0;
}
