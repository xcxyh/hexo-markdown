---
title: C/C++ 随手记
date: 2024-09-22 16:11:38
tags: C/C++ 学习
categories: C/C++
---

c++ 中的 header 文件

通过 header 文件来 声明，只需要 include 相对应的 header 文件就可以 正确的链接到对应的函数

log.h

```cpp
#ifndef LOG
#define LOG

void Log(const char* message);

#endif
```

log.cpp

```cpp
#include <iostream>
#include "log.h"

void Log(const char* message) {

    std::cout << message << std::endl;

}
```

使用：

```cpp
#include "log.h"

int main() {

    Log("hahahaha");

}
```

指针和引用：

关于   int* p  和 int *p 两种写法的说明：

int* p 其中 int* 是一种复合类型，表示 p 为 一个指向 int 的指针。

int* p1，p2； 这样写，只能说明 p1 是 一个指向 int 的指针，p2 是一个int。

int *p1 ，*p2  ，可以清晰的说明，p1 和 p2 是两个指向 int 的指针

int& ref 和 int &ref 同理。 

面对比较复杂的指针或引用的声明语句时，从右往左阅读有助于弄清其真实含义。

```cpp
#include <iostream>
#include <string.h>
using namespace std;

#define LOG(x) cout << x << endl;

int main() {
    const void* ch = nullptr;
    int var = 8;
    // 取 var 所在的内存地址，并将其标注为一个 int pointer ： int*
    int* ptr = &var;
    // 取 ptr 指向的值，并将其更改为10
    *ptr = 10;
    // ptr 为 var 所在的内存地址
    // LOG(ptr);
    // LOG(var);
    // 指针只是一个存储着内存地址的整数。
    char* buffer = new char[8];
    memset(buffer, 0, 8);
    // 指针的指针 
    char** ptrptr = &buffer;
    LOG(buffer[0] + "xx");
    LOG(ptrptr);
    delete[] buffer;
    // referances 引用只是基于 pointer 指针的一种语法糖，便于使用而已
    int a = 5;
    int& ref = a;
    ref = 7;
    LOG(ref);
}
```

const：

变量上的 const

注意：const 和 * 的相对位置，相对位置不同，const的含义也不同。

```cpp
 int* something = new int;

    *something = 11;

    const int* a = new int; // 无法改变指针 a所指向的对象的值
    // *a = 33; // error 加上了const 无法重新赋值
    a = (int*)&something; // 但是可以改变指针的指向

    int const* aa = new int; // 相对位置没有变化，写法上 与 const int* a = new int; 是等效的

    int* const b = new int; // 无法改变指针b 的指向
    *b = 44; // 可以重新赋值
    // b = (int*)&something; // error 不可以改变指针的指向

    const int* const c = new int; // 既不能重新赋值，也不能修改指针的指向

    std::cout << "val: " << *c << " addr: " << c << std::endl;

		const int &num = 1;
		num = 2; // ERROR  不允许 重新赋值，相当于 val num = 1;
```

类和方法上的const

```cpp
#include <iostream>

class Entity {

private: 
    int mX;
    int mY;

    int* mZ;
    mutable int var;
public:
    int getX() const // 加 const 表明 getX 内部 无法修改 mX 的值
    {   
        // mX = 222; // ERROR
        var = 333; // 被 mutable 修饰的变量 可以在该方法内部修改
        return mX;
    }

    void setX(int x) 
    {
        mX = x;
    }

    const int* const getZ() const // 返回一个 无法重新赋值 且无法改变指针指向的 指针， 且 getZ 内部 无法修改 mZ 的值
    {   
        // mZ = 111; // ERROR
        return mZ;
    }

};

void printEntity(const Entity& e) {  // Entity e 参数这么写，是传值，会把 e 复制一份到该函数中， 要传引用，应该是 Entity& e， 或者传指针： Entity* eptr

    // e = Entity(); // error 因为 const 限制了 无法对 e 重新赋值
    std::cout << e.getX() << std::endl;

    // e.setX(22); // error 因为方法参数上的 const 限制了无法修改 e， 所有这里的方法 只能使用被 const 修饰的方法，例如 getX

};

int main() {
    Entity e = Entity();
    e.setX(22222);
    printEntity(e);
}
```

static

class 或 struct 外的 static：link 局部可见，只对当前cpp 文件内部可见

class 或 struct 内部的 static： 与java 一致，类所有实例共享的。

构造函数 和 析构函数

虚函数（相当于java 中的被 override的函数 ） 和 纯虚函数（相当于java中的接口 或抽象方法）

虚函数表

虚函数的存在 可以让 c++ 支持多态

override 是 C++ 11 新增用于标记 override的方法，推荐写上。但是需要被override的方法不可以不写virtual

```cpp
class Entity {

public:
    Entity()
    {
        // 构造函数
        std::cout << "oncreate构造函数" << std::endl;
    }

    ~Entity()
    {
        std::cout << "ondestory析构函数" << std::endl;
    }

    virtual void print() {
        std::cout << "virtual fun can be override" << std::endl;
    }
}

class Player : public Entity
{
    void print() override {
        std::cout << "override virtual function" << std::endl;
    }
};
```

可见性 in c++  

 private，protected 和 public ，基本与java 相同。不同的是，如果不写，c++ 默认的可见性 是 private 的， 即使是 构造函数也是如此， 所以构造函数上需要 加上 public。

friend（友元）是一个关键字，它可以把其他函数或类标记为当前类的 friend。友元可以访问到类的private 变量或函数。

string in c++

```cpp
#include <iostream>
#include <array>
#include <string>

void printStr(const std::string& str) { // 传递 const reference 

    // str += "haha"; // error CONST 限制了 对 str 的更改
    std::cout << str << std::endl;
}

int main() {

    // c 语言风格定义的字符串, 表示这个字符串的 char数组 后有 一个空终止符 0
    const char* str = "hahaha";

    const wchar_t* name = L"xixi"; // 2 字节
    const char16_t* name2 = u"zoer";
    const char32_t* name3 = U"yasuio";

    // const char 数组
    std::string str2 = "xixixi";
    std::wstring str3 = L"mengduo";
    std::u16string str4 = u"thees";
    std::u32string str5 = U"threno";

    str2 += " hello";

    bool contains = str2.find("xi") != std::string::npos;

    printStr(str2);

    const char* longstr = R"(line1
    line2
    line3
    line4)";

    std::string longstr2 = R"(line1
    line2
    line3
    line4)";

    printStr(longstr2);

}
```

the new 关键字

new：在堆上找到一块连续的符合当前数据类型大小的内存块，然后返回它的内存地址（指针）。并且分配完内存后，会调用该对象的构造函数。

placement new

```cpp
// 栈上创建对象
Entity e = Entity();
// 堆上创建对象，需要手动 delete 管理其生命周期
Entity* ep = new Entity();

delete ep;

// Entity* ep2 = (Entity*)malloc(sizeof(Entity));

int* arr = new int[5];

delete[] arr;

// placement new 
```

当在栈上无法创建对象时，才在堆上去创建。栈上创建的对象不需要关心生命周期。

例如：对象的作用域需要是全局，对象的size 很大，等情况 才在堆上去创建对象，然后自己去管理该对象的生命周期。

调用 new 关键字时，会调用底层函数 malloc 去分配内存。

操作符重载 in c++

```cpp
#include <iostream>

class Vector2
{
private:
    float x, y;
public:
    Vector2(float x, float y): x(x), y(y) {}

    float getX() const
    {
        return x;
    }
    float getY() const
    {
        return y;
    }
    Vector2 Add(const Vector2& other) const
    {
        return Vector2(x + other.x, y + other.y);
    }

    Vector2 Mutiplty(const Vector2& other) const
    {
        return Vector2(x * other.x, y * other.y);
    }

    Vector2 operator+(const Vector2& other) const
    {
        return Add(other);
    }

    Vector2 operator*(const Vector2& other) const
    {
        return Mutiplty(other);
    }

    bool operator==(const Vector2& other) const
    {
        return x == other.x && y == other.y;
    }

    bool operator!=(const Vector2& other) const
    {
        return !(*this == other);
    }

};

std::ostream& operator<<(std::ostream& stream, Vector2& other)
{
    stream << other.getX() << ", " << other.getY();
    return stream;
}

int main() {

    Vector2 v1(1.0f, 2.0f);

    Vector2 v2(2.2f, 3.3f);

    Vector2 v3 = v1 + v2;

    std::cout << v1 << std::endl;

    std::cout << v3.getX() << ", " << v3.getY() << std::endl;

    std::cout << (v1 != v2) << std::endl;

}
```

this 是指向实例对象的指针

智能指针

作用域指针 unique_ptr

引用计数指针 shared_ptr

弱引用指针 weak_ptr

```cpp
#include <iostream>
#include <memory>

class Entity
{

    Entity()
    {
        std::cout << "create entity" << std::endl;
    }

    ~Entity()
    {
        std::cout << "destroy entity" << std::endl;
    }
public:
    void print() {}

};

int main() {

    {
        std::unique_ptr<Entity> entity = std::make_unique<Entity>();
        entity->print();
    }
    // 超出作用域后自动销毁

    {   
        std::shared_ptr<Entity> shared2;
        {
            std::shared_ptr<Entity> sharedEntity = std::make_shared<Entity>();
            shared2 = sharedEntity; // 引用计数 + 1
            sharedEntity->print();
        }

    }
    // 引用计数为0 后才会自动销毁
    {   
        std::weak_ptr<Entity> weakptr;
        {
            std::shared_ptr<Entity> sharedEntity = std::make_shared<Entity>();
            weakptr = sharedEntity; // 不会增加 引用计数
            sharedEntity->print();
        }
        // 在这里就会自动销毁
        // weak ptr 弱引用
    }

}
```

C++ 变量初始化列表：

```cpp
Vector2(float x, float y): x(x), y(y) {}

// equals 这样写，变量会被初始化两次，用初始化列表，则只初始化一次
Vector2(float x, float y) {
	this->x = x;
	this->y = y;
}
```

C++ 中的 lambda 表达式

![Lambda](https://raw.githubusercontent.com/xcxyh/xcxyh.github.io/image-save/images/2024202409221610799.png)

1. capture 子句（在 C++ 规范中也称为 Lambda 引导。）
2. 参数列表（可选）。 （也称为 Lambda 声明符）
3. mutable 规范（可选）。
4. exception-specification（可选）。
5. trailing-return-type（可选）。
6. Lambda 体。

capture 子句：Lambda 可在其主体中引入新的变量（用 C++14），它还可以访问（或“捕获”）周边范围内的变量。空 capture 子句 `[ ]`指示 lambda 表达式的主体不访问封闭范围中的变量。`[&]`
 表示通过引用捕获引用的所有变量，而 `[=]`表示通过值捕获它们。可以使用默认捕获模式，然后为特定变量显式指定相反的模式。

```cpp
[&total, factor]
[factor, &total]
[&, factor]
[=, &total]
```

**C++ #include " " 与 <>有什么区别？**

在C++中，使用#include指令可以将头文件包含到源代码文件中。头文件通常包含了函数、类、结构体和变量的声明，以及其他预处理指令。

在使用#include指令时，可以使用双引号或尖括号来指定头文件的路径。使用双引号时，编译器会首先在当前源代码文件所在的目录中查找头文件；如果找不到，则会在编译器设置的路径中查找。而使用尖括号时，编译器只会在预定义的系统路径中查找头文件。

因此，使用双引号可以用来包含自己编写的头文件，而使用尖括号则用来包含系统提供的头文件。另外，使用双引号时，编译器还会在包含头文件的源文件的同一目录中查找头文件，这有助于组织相对路径的头文件。