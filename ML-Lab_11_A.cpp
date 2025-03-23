#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <chrono>

using namespace std;
using namespace chrono;

// Function to calculate the sum of elements in an array
int calculateSum(const vector<int>& arr) {
    int sum = 0;
    for (int num : arr) {
        sum += num;
    }
    return sum;
}

// Function to search for a key element in the array
bool searchKey(const vector<int>& arr, int key) {
    for (int num : arr) {
        if (num == key) {
            return true;
        }
    }
    return false;
}

int main() {
    int n, key;

    // Input the size of the array
    cout << "Enter the size of the array (n): ";
    cin >> n;

    // Input the key to search
    cout << "Enter the key to search: ";
    cin >> key;

    // Generate random array
    srand(time(0));
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        arr[i] = rand() % 1000; // Random integers between 0 and 999
    }

    // Measure time for sum calculation
    auto startSum = high_resolution_clock::now();
    int sum = calculateSum(arr);
    auto endSum = high_resolution_clock::now();
    cout << "Sum of elements: " << sum << "\n";
    cout << "Execution time for sum calculation: " 
         << duration_cast<microseconds>(endSum - startSum).count() << " microseconds.\n";

    // Measure time for key search
    auto startSearch = high_resolution_clock::now();
    bool found = searchKey(arr, key);
    auto endSearch = high_resolution_clock::now();
    cout << "Key " << (found ? "found" : "not found") << " in the array.\n";
    cout << "Execution time for key search: " 
         << duration_cast<microseconds>(endSearch - startSearch).count() << " microseconds.\n";

    return 0;
}
