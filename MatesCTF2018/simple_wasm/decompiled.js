///////////////////////////////////////////////////
let mem=new Array(64*1024*256)
mem.fill(0)

// f0: i32 i32 -> i32
function dist(a, b) {
    if (a < b) {
        return b - a
    } else {
        return a - b
    }
}

// f1: i32  -> i32
function f1(maxdiff) {
          // 1

    let cnt=0;

    let l1=0;
    let l2=0;
    let l3=0;

    while (l1 < mem[0] - 1) {

        if (dist(mem[l1+1], mem[l1+2]) <= maxdiff) {
            cnt += 1
        }

        l1 += 1
    }

    return cnt
}



// f2:
function f2() {
    let local_0 = 0;
    while (true) {

        if (local_0 < mem[0]) {

            if (mem[local_0 + 1] < 9) {

                mem[local_0 + 1] += 1;
                break

           } else {

               mem[local_0 + 1] = 0;
               local_0 += 1;
           }

       } else {

           mem[local_0 + 1] = 1;
           mem[0] += 1;
           break

       }

   }
}

// f3: i32 i32 -> i32
function safe_mod(a, b) {
    if (b === 0) {
        return 0
    }

    return a % b
}

// f4: i32 i32 -> i32
function safe_div(a, b) {
    if (b === 0) {
        return 0
    }

    if (a === -2147483648 && b === -1) {
        return 0
    }

    return Math.floor(a / b)
}

function start(number) {
    // i32
    let counter = 0

    while (number > 0) {
        mem[counter+1] = safe_mod(number, 10);
        number = safe_div(number, 10);
        counter += 1
    }

    mem[0] = counter;
    return counter;
}

// count: i32 -> i32
function count(a, b, c, d) {
               //0, i, 1, 0
    // i32
    let l0 = 0;
    // i32
    let l1 = a;

    while (l1 < b) {
        if(f1(c) <= d) l0 += 1

        f2();
        l1 += 1
    }

    return l0;
}

function check(number) {
    start(1);
    var result = 0;
    for (let i = 0; i < 1000; ++i) {
        start(1)
        console.log(i,count(0, i, 1, 0))
    }

    return 

    if (result == 14827558276137) {
      console.log('matesctf{' + number.toString() + '}');
    }
    else {
      console.error('Try again!');
    }
}

check(2**35)

