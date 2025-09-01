#include <iostream>
#include <ctime>
#include <map>
using namespace std;
class Wheeler
{
public:
    string type;
    string num;
    time_t entry;

    Wheeler(string number, string name)
    {
        type = name;
        num = number;
        entry = time(0);
    }
    virtual void customer_details()
    {
        cout << "Vehicle name - " << type << "Number - " << num << endl;
    }
    virtual ~Wheeler() {};
};
class Car : public Wheeler
{
public:
    Car(string number) : Wheeler(number, "Car") {}; 
    void customer_details() override 
    {
        cout << "Car - number : " << num << endl;
    }
};
class Bike : public Wheeler
{
public:
    Bike(string number) : Wheeler(number, "Bike") {};
    void customer_details() override
    {
        cout << "Bike - number : " << num << endl;
    }
};

class slotbooking
{
private:
    int totalslots;
    map<int, Wheeler *> slots;

public:
    slotbooking(int limit)
    {
        totalslots = limit;
    }
    bool filled()
    {
        return slots.size() >= totalslots; 
    }
    int parking(string num, string type)
    {
        if (filled())
        {
            cout << "No slots are available , parking is full" << endl;
            return -1;
        }
        int cnt = 1;
        while (slots.find(cnt) != slots.end())
        {
            cnt++;
        }
        if (type == "Car")
        {
            slots[cnt] = new Car(num); 
        }
        else if (type == "Bike")
        {
            slots[cnt] = new Bike(num);
        }
        else
        {
            cout << "Invalid entry...!" << endl;
            return -1;
        }
        cout << "Vehicle is parked at slot number : " << cnt << endl;
        return cnt;
    }
    void remove(int cnt)
    {
        if (slots.find(cnt) == slots.end())
        {
            cout << "No parking slot is available with this slot number " << endl;
            return;
        }
        Wheeler *v = slots[cnt];
        time_t exit = time(0);
        double duration = difftime(exit, v->entry) / 60;
        double fee = 5 * duration;
        cout << "Your vehicle is removed from slot - " << cnt << endl;
        v->customer_details();
        cout << "Time taken : " << duration << " minutes " << endl;
        cout << "\nYou should pay : " << fee << " rupees only (5 rupees per min)" << endl;
        delete v;
        slots.erase(cnt);
    }
    void display()
    {
        cout << "Current parking status" << endl;
        if (slots.empty())
        {
            cout << "Slots are empty" << endl;
            return;
        }
        for (auto &it : slots)
        {
            cout << "Slot " << it.first << " -->> ";
            it.second->customer_details();
        }
    }

    ~slotbooking()
    {
        for (auto &it : slots)
        {
            delete it.second;
        }
    }
};

int main()
{
    int k, l;
    cout << "How many slots are available totally : ";
    cin >> k;
    slotbooking park(k);
    while (true)
    {
        cout << "--------------------------------------------------------\n";
        cout << "                   Welcome to IIIT Raichur\n";
        cout << "Choose your choice " << "\n1. Park a vehicle\n2. remove vehicle \n3. Current booking status \n4. Exit ";
        cout << "\nEnter : ";
        cin >> l;
        if (l == 1)
        {
            string num, name;
            cout << "Enter vehicle number : ";
            cin.ignore();
            getline(cin,num);
            cout << "Enter vehicle type (Car/Bike) : ";
            cin >> name;
            park.parking(num, name);
        }
        else if (l == 2)
        {
            int mark;
            cout << "Enter the slot number to be removed : ";
            cin >> mark;
            park.remove(mark);
        }
        else if (l == 3)
        {
            park.display();
        }
        else if (l == 4)
        {
            cout << "Exiting...!";
            break;
        }
        else
        {
            cout << "Invalid input\n";
        }
    }
    return 0;
}