typedef struct {
    int quote_len;
    char *quote;
    int name_len;
    char *name;
} wisdom_t;

char const *default_name = "Neonate\n";

int templeWisdom = 0;
wisdom_t *temple[0x100];
char *wisdom[8] = {};
char *prohpets[8] = {};

void horizon() {
    // print contents of temple.txt
}

void scribe_store(wisdom_t *wisdom_struct) {
    if (templeWisdom > 0xff) {
        puts("We have nothing else to offer you. Seek another temple.");
        exit(0);
    }

    temple[templeWisdom] = wisdom_struct;
    templeWisdom++;

    // return templeWisdom
}

wisdom_t *make_wisdom() {
    wisdom_t *wisdom_struct = mm_malloc(sizeof(wisdom_t));
    size_t index = rand();

    // some transformation to index

    wisdom_struct->quote = wisome[index];
    wisdom_struct->quote_len = strlen(wisdom[index]);
    wisdom_struct->name = prohpets[index];
    wisdom_struct->name_len = strlen(prohpets[index]);

    scribe_store(wisdom_struct);

    return wisdom_struct;
}

void readint() {
    char buffer[0x100];

    if(fgets(buffer, sizeof(buffer), stdin) != 0) {
        int val = atoi(buffer);
        if (val < 0) {
            return 0;
        } else {
            return val;
        }
    } else {
        return 0;
    }
}

wisdom_t *scribe_recall(int index) {
    if (index >= templeWisdom) {
        puts("You will find no knowledge of this here.");
        return NULL;
    }

    wisdom_t *wisdom_struct = temple[index];
    if (wisdom_struct == NULL) {
        puts("You have already studied this knowledge.");
    }

    return wisdom_struct;
}

void print_wisdom(wisdom_t *wisdom_struct) {
    write(0x1, wisdom_struct->quote, wisdom_struct->quote_len);
    write(0x1, "\t - ", 0x4);
    write(0x1, wisdom_struct->name, wisdom_struct->name_len);
}

void free_wisdom(wisdom_t *wisdom_struct) {
    if (strcmp(wisdom_struct->name, default_name) == 0) {
        mm_free(wisdom_struct->quote);
    }

    mm_free(wisdom_struct);

    for (int i = 0; i < templeWisdom; i++) {
        if (temple[i] == wisdom_struct) {
            temple[i] = NULL;
            break;
        }
    }
}

void take_wisdom() {
    printf("What wisdom do you seek?: ");

    int index = readint();
    wisdom_t *wisdom_struct = scribe_recall(index);
    if (wisdom_struct != NULL) {
        print_wisdom(wisdom_struct);
        free_wisdom(wisdom_struct);
    }
}

int readbytes(void *buffer, int len) {
    fgets(buffer, len+1, stdin);
    return len+1;
}

void give_wisdom() {
    printf("How much wisdom do you hold?: ");
    int quote_len = readint();
    if (quote_len == 0x0) {
        puts("Your wisdom is not wanted here.");
        return 0;
    }

    printf("What is your wisdom?: ");

    wisdom_t *wisdom_struct = mm_malloc(sizeof(wisdom_t));

    char *quote = mm_malloc(quote_len);
    int read_len = readbytes(quote, quote_len);

    wisdom_struct->quote = quote;
    wisdom_struct->quote_len = read_len; // quote_len + 1
    wisdom_struct->name = default_name;
    wisdom_struct->name_len = strlen(default_name);

    scribe_store(wisdom_struct);
}

void modify_wisdom() {
    printf("What wisdom do you wish to rethink?: ");

    int index = readint();
    if (index <= 0x7) {
        puts("That's not your wisdom!");
        return;
    }

    wisdom_t *wisdom_struct = scribe_recall(index);
    if (wisdom_struct != NULL) {
        printf("(%lu) How do you see this differently?: ", wisdom_struct->quote_len);
        readbytes(wisdom_struct->quote, wisdom_struct->quote_len);
    }
}

void seek_divinity() {
    puts("\nChild, what do you seek?");
    puts("[1] Take wisdom");
    puts("[2] Give wisdom");
    puts("[3] Rethink wisdom");
    printf("Your choice: ");

    int option = readint();

    switch(option) {
        case 1: {
            take_wisdom();
            break;
        }
        case 2: {
            give_wisdom();
            break;
        }
        case 3: {
            modify_wisdom();
            break;
        }
        default: {
            puts("What you ask for cannot be found here.")
            break;
        }
    }
}

int main() {
    srand(time(0));

    horizon();

    for (int i = 0; i <= 0x7; i++) {
        make_wisdom();
    }

    seek_divinity();
}