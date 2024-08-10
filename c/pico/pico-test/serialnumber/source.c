#include "source.h"
#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/unique_id.h"

int main(int argc, char const *argv[])
{
    stdio_init_all();

    int len = 2 * PICO_UNIQUE_BOARD_ID_SIZE_BYTES + 1;
    uint8_t serialno[len];
    pico_get_unique_board_id_string((char *)serialno, len);

    while (true)
    {
        printf("Printing Pico serial number: ");
        printf(serialno);
        printf("\n");
        sleep_ms(5000);
    }
    
    return 0;
}
