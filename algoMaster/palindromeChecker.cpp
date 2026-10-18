#include<iostream>
// #include <bits/stdc++.h>
using namespace std;





bool palindromeChecker(string s){
    string temp =s ;
    std::reverse(temp.begin(),temp.end());
    return temp==s;
}

int main(){

    string temp ;
    std::cout<<"Enter the string : ";
    std::cin>>temp;




    bool trueFalse = palindromeChecker(temp);
    if(trueFalse){
        std::cout<<"this is teh palindrome";
    }else{
        std::cout<<"This is not the palindrome";
    }
    return 0;





























    //this is the end of the comment

}