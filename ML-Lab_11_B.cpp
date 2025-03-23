#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <chrono>
#include <thread>
#include <atomic>

using namespace std;
using namespace chrono;

atomic<int> globalSum(0); // Atomic variable for thread-safe sum calculation
atomic<bool> keyFound(false); // Atomic variable to check if the key is found

// Function to calculate the sum in a partition
void calculatePartitionSum(const vector<int>& arr, int start, int end) {
    int localSum = 0;
    for (int i = start; i < end; i++) {
        localSum += arr[i];
    }
    globalSum += localSum; // Add to global sum
}

// Function to search for the key in a partition
void searchPartitionKey(const vector<int>& arr, int start, int end, int key) {
    for (int i = start; i < end; i++) {
        if (arr[i] == key) {
            keyFound = true;
            return;
        }
    }
}

int main() {
    int n, key, numThreads;

    // Input the size of the array and the number of threads
    cout << "Enter the size of the array (n): ";
    cin >> n;
    cout << "Enter the number of threads: ";
    cin >> numThreads;
    cout << "Enter the key to search: ";
    cin >> key;

    // Generate random array
    srand(time(0));
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        arr[i] = rand() % 1000; // Random integers between 0 and 999
    }

    // Partition size
    int partitionSize = n / numThreads;

    // Measure time for threaded sum calculation
    auto startSum = high_resolution_clock::now();
    vector<thread> sumThreads;
    for (int i = 0; i < numThreads; i++) {
        int start = i * partitionSize;
        int end = (i == numThreads - 1) ? n : start + partitionSize;
        sumThreads.push_back(thread(calculatePartitionSum, ref(arr), start, end));
    }
    for (auto& t : sumThreads) {
        t.join();
    }
    auto endSum = high_resolution_clock::now();
    cout << "Sum of elements: " << globalSum.load() << "\n";
    cout << "Execution time for threaded sum calculation: " 
         << duration_cast<microseconds>(endSum - startSum).count() << " microseconds.\n";

    // Measure time for threaded key search
    auto startSearch = high_resolution_clock::now();
    vector<thread> searchThreads;
    for (int i = 0; i < numThreads; i++) {
        int start = i * partitionSize;
        int end = (i == numThreads - 1) ? n : start + partitionSize;
        searchThreads.push_back(thread(searchPartitionKey, ref(arr), start, end, key));
    }
    for (auto& t : searchThreads) {
        t.join();
    }
    auto endSearch = high_resolution_clock::now();
    cout << "Key " << (keyFound.load() ? "found" : "not found") << " in the array.\n";
    cout << "Execution time for threaded key search: " 
         << duration_cast<microseconds>(endSearch - startSearch).count() << " microseconds.\n";

    return 0;
}
