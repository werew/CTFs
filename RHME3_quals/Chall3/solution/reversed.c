# Add player

char user_input[0x100]

struct player {  // 0x18 (24)
    +0x00 int attack
    +0x04 int defense
    +0x08 int speed
    +0x0c int precision
    +0x10 void* name ----> (allocated string max 0x100)
                           (len is strlen(user_input)+1)
}



delete_player(){

    int index = atoi(user_input);
    if (index < 0xa && players[index] != NULL){
        // REMOVE
        player = players[index]
        players[index] = NULL;
        free(player->name);
        free(player);
    }
}


select_player(){
    int index = atoi(user_input);
    if (index < 0xa && players[index] != NULL){
        selected = players[index]
        show_player_func(selected);
    }
}


set_name(){
    if (strlen(user_input) <= strlen(old_name)){
        // Reallocate
        selected.name = realloc(strlen(user_input)+1)
    } 
    // Copy name
}

show_player(){
    if ( selected != NULL){
        show_player_func();
    }
}

