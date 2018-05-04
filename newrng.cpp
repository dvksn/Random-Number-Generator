#include <iostream>
#include <cmath>
#include <fstream>
using namespace std;
const long long int  m2=2147483647, a2=1797657,  a1=53889, m1=2147483648;
const int c2=1607, seed2=17, c1=1333, seed1 =13;
          
     
long long int ran (long long int a, long long int m , int c, int seed){
	long long int number= (a*seed+c)%m;
	return number;
}

int main() {
	long long int rand1=seed1,rand2=seed2;
    ofstream myfile ("randomNumbersNew.txt");
  
    for(int i=0;i<10000;i++)
    {
        rand1= ran(a1,m1,c1,rand1);
        rand2= ran(a2,m2,c2,rand2);
        long long int random_number=(rand1-rand2+m1)%m1;
        // double random_number_red = random_number/(double)(pow(10,10));
        double random_number_red = random_number/(double)m1;

        
        if (myfile.is_open())
        {
            myfile << random_number_red <<"\n";
        }
        // cout<<random_number<<endl;
    }
    myfile.close();
    system("/usr/bin/python test.py randomNumbersNew.txt");
    return 0;
}
