#include <sys/types.h>
#include <pwd.h>
#include <iostream>

struct POSIX_USER{
    std::string username;
    std::string shell;
    bool shellLogin;
    POSIX_USER * next;
};

class sysEnum {
    private:
        POSIX_USER * usrList = NULL;
        struct POSIX_USER pos1;
        bool subStr(std::string input, std::string substr);
    public:
        void listUsers();
        void getUsers();
};

void sysEnum::listUsers() {
    POSIX_USER * tmp;
    tmp = usrList;
    while(tmp != NULL) {
        std::cout << tmp->username << std::endl;
        tmp = tmp->next;
    }
}

/**
 * List all users in the current
 * system. This will only work for posix
 * based systems.
*/
void sysEnum::getUsers() {
    while (true) {
        errno = 0;
        passwd* entry = getpwent();
        if (!entry) {
            if (errno) {
                std::cerr << "Error reading password database" << std::endl;
            }
            break;
        }
        // Create new user
        POSIX_USER * tmp = new POSIX_USER();
        // Assign the struct params
        tmp->shell = entry->pw_shell;
        tmp->username = entry->pw_name;
        // Check if the user can login to shell
        if(subStr(tmp->shell, "nologin")) {
            tmp->shellLogin = false;
        } else {
            tmp->shellLogin = true;
        }
        tmp->next = usrList;
        usrList = tmp;
    }
    endpwent();
}

bool sysEnum::subStr(std::string input, std::string substr) {
    int pos = 0;
    int index;
    while((index = input.find(substr, pos)) != std::string::npos) {
        return true;
    }
    return false;
}