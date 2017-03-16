#include <iostream>
#include <string>
#include <fstream>
#include <dirent.h>
#include <stdio.h>
#include <sys/stat.h>
#include <vector>
#include <unistd.h>
using namespace std;


string encrypt(string input);
bool is_file_exist(const char *fileName);
void encryptFile(string filePath);
void goThroughPathOrFile(string path, bool isRecursive, bool isFirstTime);
vector<string> filesInDir(string dirPath);


// arguments can be directorys or files
int main(int argc, char **argv){
    bool isRecursive = false;
    int c = 0;
    opterr = 0;
    
    while ( (c = getopt(argc, argv, "r")) != -1) {
        switch (c) {
                case 'r':
                isRecursive = true;
                break;
            default:
                cerr << "Unknown option. \n";
                cerr << "Usage: -r : Recursively go through the directory";
                exit(-1);
                break;
        }
    }
    if (argc == 1) {
        string str = "";
        while (cin >> str, !cin.eof()) {
            cout << encrypt(str) << endl;
        }
    }else {
        for (int i = optind; i < argc; i++){
            goThroughPathOrFile(argv[i], isRecursive, true);
        }
    }
    return 0;
}


// check file is exist
bool is_file_exist(const char *fileName){
    ifstream infile(fileName);
    return infile.good();
}

void encryptFile(string filePath) {
    ifstream file;
    cout << "File: " << filePath << ": ";
    if (!is_file_exist(filePath.c_str())) {
        cout << "file not found!" << endl;
        cout << "----------" << endl;
        return;
    }
    cout << endl;
    file.open(filePath);
    string content = "";
    while (file >> content, !file.eof()) {
        cout << encrypt(content) << endl;
    }
    cout << "----------" << endl;
    file.close();
}

// encrypt the string
string encrypt(string input) {
    for (int i = 0; i < input.length(); i++){
        char cha = input[i];
        if ((cha != 'z' || cha != 'Z') && isalpha(cha)) {
            cha += 1;
            input[i] = cha;
        }
        if (cha == 'z') {
            input[i] = 'a';
        }
        if (cha == 'Z') {
            input[i] = 'A';
        }
    }
    return input;
}

string joinPath(string dir, string path) {
    if (dir[dir.length()-1] == '/') {
        return dir + path;
    }else {
        return dir + "/" + path;
    }
}

vector<string> filesInDir(string dirPath) {
    DIR           *d;
    struct dirent *dir;
    d = opendir(dirPath.c_str());
    vector<string> files = {};
    if (d){
        while ((dir = readdir(d)) != NULL){
            //            printf("%s\n", dir->d_name);
            string fileName = dir->d_name;
            if (fileName[0] == '.') continue;
            files.push_back( joinPath(dirPath, fileName));
            cout << dirPath << endl;
            cout << fileName << endl;
        }
        closedir(d);
    }
    return files;
}

void goThroughPathOrFile(string path, bool isRecursive, bool isFirstTime) {
    struct stat s;
    if( stat(path.c_str(),&s) == 0 ){
        if( s.st_mode & S_IFDIR){
            if (isRecursive || isFirstTime) {
                vector<string> files = filesInDir(path);
                for (int i = 0; i<files.size(); i++) {
                    goThroughPathOrFile(files[i], isRecursive, false);
                }
            }
        }
        else if( s.st_mode & S_IFREG ){
            encryptFile(path);
        }
        else{
            return;
            //something else
        }
    }else{
        cerr << "Unexpected error hapand when in " << path << endl;
    }
}

