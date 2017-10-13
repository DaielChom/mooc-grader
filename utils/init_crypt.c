#include <iostream>
#include <fstream>

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

    if (argc!=2) {
        cerr << "call syntax (encrypts or decrypts file to stdout):\n    " << argv[0] << " file\n";
        return(-1);
    }

    ifstream in(argv[1]);
    string s((istreambuf_iterator<char>(in)), istreambuf_iterator<char>());

    cout << encryptDecrypt(s) ;

    return 0;
}