
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <unistd.h>


using namespace std;

string encryptDecrypt(string toEncrypt) {
    char key[10] = ##KEYC##; //Any chars will work, in an array of any size
    string output = toEncrypt;

    for (int i = 0; i < toEncrypt.size(); i++)
        output[i] = toEncrypt[i] ^ key[i % (sizeof(key) / sizeof(char))];

    return output;
}

int main(int argc, const char * argv[])
{

    if (argc==1) {
        cerr << "call syntax (runs an encrypted python script):\n    " << argv[0] << " script.epy args...\n";
        return(-1);
    }
    
    ifstream in(argv[1]);
    string s((istreambuf_iterator<char>(in)), istreambuf_iterator<char>());
    string ds = encryptDecrypt(s);
    
    string python_cmd = "python -";
    
    for (int i=2; i<argc; i++) {
        python_cmd = python_cmd + " " + string(argv[i]);
    }
    
    FILE *output;
    output = popen (python_cmd.c_str(), "w");
    if (!output) { cerr << "call error\n"; return(-1); }
    fprintf(output, "%s", ds.c_str());
    if (pclose (output) != 0) { cerr << "call error\n"; return(-1); }
    
    
    return 0;
}