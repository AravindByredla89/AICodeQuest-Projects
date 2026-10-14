
#include <iostream>
#include <random>
using namespace std;


int randomGenerator(int n){
    int randomNumber = rand()%n;



    return randomNumber+1;
}



// a comment to fill this with the next upcoming algorithmsd 


















int main() {
    int n;
    cin >> n;

    random_device rd;
    mt19937 gen(rd());

    uniform_int_distribution<int> dist(0, n);

    for (int i = 0; i < 50; i++) {
        cout << dist(gen) << '\n';
    }

    return 0;
}
