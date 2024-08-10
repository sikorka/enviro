#include "source.h"
#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/unique_id.h"

int main(int argc, char const *argv[])
{
    stdio_init_all();

    int len = 2 * PICO_UNIQUE_BOARD_ID_SIZE_BYTES + 1;
    uint8_t buff[len];
    pico_get_unique_board_id_string((char *)buff, len);

    printf("Printing Pico serial number: ");
    
    while (true)
    {
        printf(buff);
        sleep_ms(1000);
    }

    return 0;
}
