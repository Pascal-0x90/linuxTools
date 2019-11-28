#include <iostream>
#include "LinUserFinder.h"

int main() {
    sysEnum sys = sysEnum();
    sys.getUsers();
    sys.listUsers();
}