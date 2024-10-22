```
0x6022b0:       0x602   0x0                                                                                                                                                                   
0x6022c0:       0x0     0x0                                                                                                                                                                   
0x6022d0:       0x0     0x31                                                                                                                                                                  
0x6022e0:       0x602d12        0x63de0afcce0e5781                                                                                                                                            
0x6022f0:       0x4141414141414141      0x4141414141414141



0x7ffff7fff270: 0x0     0x0
0x7ffff7fff280: 0x0     0x0
0x7ffff7fff290: 0x0     0x31
0x7ffff7fff2a0: 0x7ffff7fffad0  0x7ffff7fff010
0x7ffff7fff2b0: 0x4141414141414141      0x4141414141414141

0x7ffff7fff270: 0x602   0x0
0x7ffff7fff280: 0x0     0x0
0x7ffff7fff290: 0x0     0x31
0x7ffff7fff2a0: 0x7ff9f6b6f     0x0
0x7ffff7fff2b0: 0x0     0x0


```








# globals

- heroes_skills_sizes: 0x60 (size of mallocd desc)
- chairs: 0x60 (4 bytes bool)
- heroes: 0xa0 (ptr to mallocd desc)
- number_heroes: 0x8

# new_hero

- if number_heros < 0x14: bump allocate hero in free chair

# edit_skill

- if i [0, 0x13] && chairs[i]:
 - read in heroes[i] up to skill_size
 - *(undefined *)((long)(int)new_siz + heroes[i]) = 0; #null term - null overflow

# kick_hero

- if i [0, 0x13] && chairs[i]:
 - free(heros[i])
 - chair[i] = 0

# show_hero_skill

- if i [0, 0x13] && heros[i]:
 - show(heros[i]) # show freed mem


 

- 

