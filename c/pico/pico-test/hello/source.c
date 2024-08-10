#include "source.h"
#include <stdio.h>
#include "pico/stdlib.h"

int main(int argc, char const *argv[])
{
    stdio_init_all();

    while (true)
    {
        printf("Hello World");
        sleep_ms(1000);
    }

    return 0;
}
