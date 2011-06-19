#include <iostream>

using namespace std;
class parent_class {
	public:
		int i;
		parent_class(void) {
			int t=0;
			i=31337;
			cout << "We are constructing the parent_class" << endl;
		}
		~parent_class(void) {
			cout << "We are destructing the parent_class" << endl;
		}
	private:
		void private_func(void) {
			cout << "private_func" << endl;
		}
};

class child_class : parent_class {
	public:

};


int main(int argc, char **argv) {
	parent_class test1;
	child_class test2;
	//cout << "test2.i = " << test2.i << endl;
}
