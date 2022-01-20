contract Contract {
    function main() {
        memory[0x40:0x60] = 0x80;
    
        if (msg.data.length < 0x04) { revert(memory[0x00:0x00]); }
    
        var var0 = msg.data[0x00:0x20] / 0x0100000000000000000000000000000000000000000000000000000000 & 0xffffffff;
    
        if (var0 == 0x02afa7a0) {
            // Dispatch table entry for 0x02afa7a0 (unknown)
            var var1 = msg.value;
        
            if (var1) { revert(memory[0x00:0x00]); }
        
            var1 = 0x0142;
            var var2 = msg.data[0x04:0x24] & 0xffffffffffffffffffffffffffffffffffffffff;
            var2 = func_050E(var2);
            var temp0 = memory[0x40:0x60];
            memory[temp0:temp0 + 0x20] = var2;
            var temp1 = memory[0x40:0x60];
            return memory[temp1:temp1 + (temp0 + 0x20) - temp1];
        } else if (var0 == 0x0339f300) {
            // Dispatch table entry for revise(uint256,bytes32)
            var1 = msg.value;
        
            if (var1) { revert(memory[0x00:0x00]); }
        
            var1 = 0x0191;
            var2 = msg.data[0x04:0x24];
            var var3 = msg.data[0x24:0x44];
            revise(var2, var3);
            stop();
        } else if (var0 == 0x23de8635) {
            // Dispatch table entry for 0x23de8635 (unknown)
            var1 = msg.value;
        
            if (var1) { revert(memory[0x00:0x00]); }
        
            var1 = 0x01be;
            var2 = msg.data[0x04:0x24];
            func_06CE(var2);
            stop();
        } else if (var0 == 0x24b04905) {
            // Dispatch table entry for gift()
            var1 = msg.value;
        
            if (var1) { revert(memory[0x00:0x00]); }
        
            var1 = 0x01d5;
            gift();
            stop();
        } else if (var0 == 0x2e1a7d4d) {
            // Dispatch table entry for withdraw(uint256)
            var1 = msg.value;
        
            if (var1) { revert(memory[0x00:0x00]); }
        
            var1 = 0x0202;
            var2 = msg.data[0x04:0x24];
            withdraw(var2);
            stop();
        } else if (var0 == 0x47f57b32) {
            // Dispatch table entry for retract()
            var1 = msg.value;
        
            if (var1) { revert(memory[0x00:0x00]); }
        
            var1 = 0x0219;
            retract();
            stop();
        } else if (var0 == 0x6bc344bc) {
            // Dispatch table entry for payforflag(string)
            var1 = msg.value;
        
            if (var1) { revert(memory[0x00:0x00]); }
        
            var1 = 0x0282;
            var temp2 = msg.data[0x04:0x24] + 0x04;
            var temp3 = msg.data[temp2:temp2 + 0x20];
            var temp4 = memory[0x40:0x60];
            memory[0x40:0x60] = temp4 + (temp3 + 0x1f) / 0x20 * 0x20 + 0x20;
            memory[temp4:temp4 + 0x20] = temp3;
            memory[temp4 + 0x20:temp4 + 0x20 + temp3] = msg.data[temp2 + 0x20:temp2 + 0x20 + temp3];
            var2 = temp4;
            payforflag(var2);
            stop();
        } else if (var0 == 0x70a08231) {
            // Dispatch table entry for balanceOf(address)
            var1 = msg.value;
        
            if (var1) { revert(memory[0x00:0x00]); }
        
            var1 = 0x02c5;
            var2 = msg.data[0x04:0x24] & 0xffffffffffffffffffffffffffffffffffffffff;
            var2 = balanceOf(var2);
            var temp5 = memory[0x40:0x60];
            memory[temp5:temp5 + 0x20] = var2;
            var temp6 = memory[0x40:0x60];
            return memory[temp6:temp6 + (temp5 + 0x20) - temp6];
        } else if (var0 == 0x83211805) {
            // Dispatch table entry for 0x83211805 (unknown)
            var1 = msg.value;
        
            if (var1) { revert(memory[0x00:0x00]); }
        
            var1 = 0x02f0;
            var2 = func_0FA5();
            var temp7 = memory[0x40:0x60];
            memory[temp7:temp7 + 0x20] = !!var2;
            var temp8 = memory[0x40:0x60];
            return memory[temp8:temp8 + (temp7 + 0x20) - temp8];
        } else if (var0 == 0x8da5cb5b) {
            // Dispatch table entry for owner()
            var1 = msg.value;
        
            if (var1) { revert(memory[0x00:0x00]); }
        
            var1 = 0x031f;
            var2 = owner();
            var temp9 = memory[0x40:0x60];
            memory[temp9:temp9 + 0x20] = var2 & 0xffffffffffffffffffffffffffffffffffffffff;
            var temp10 = memory[0x40:0x60];
            return memory[temp10:temp10 + (temp9 + 0x20) - temp10];
        } else if (var0 == 0x8df6fbcc) {
            // Dispatch table entry for 0x8df6fbcc (unknown)
            var1 = msg.value;
        
            if (var1) { revert(memory[0x00:0x00]); }
        
            var1 = 0x0376;
            var2 = func_0FDD();
            var temp11 = memory[0x40:0x60];
            memory[temp11:temp11 + 0x20] = var2;
            var temp12 = memory[0x40:0x60];
            return memory[temp12:temp12 + (temp11 + 0x20) - temp12];
        } else if (var0 == 0x9189fec1) {
            // Dispatch table entry for guess(uint256)
            var1 = msg.value;
        
            if (var1) { revert(memory[0x00:0x00]); }
        
            var1 = 0x03b7;
            var2 = msg.data[0x04:0x24];
            guess(var2);
            stop();
        } else if (var0 == 0x94bd7569) {
            // Dispatch table entry for codex(uint256)
            var1 = msg.value;
        
            if (var1) { revert(memory[0x00:0x00]); }
        
            var1 = 0x03e4;
            var2 = msg.data[0x04:0x24];
            var2 = codex(var2);
            var temp13 = memory[0x40:0x60];
            memory[temp13:temp13 + 0x20] = var2;
            var temp14 = memory[0x40:0x60];
            return memory[temp14:temp14 + (temp13 + 0x20) - temp14];
        } else if (var0 == 0xa6f2ae3a) {
            // Dispatch table entry for buy()
            var1 = msg.value;
        
            if (var1) { revert(memory[0x00:0x00]); }
        
            var1 = 0x0417;
            buy();
            stop();
        } else if (var0 == 0xa9059cbb) {
            // Dispatch table entry for transfer(address,uint256)
            var1 = msg.value;
        
            if (var1) { revert(memory[0x00:0x00]); }
        
            var1 = 0x0464;
            var2 = msg.data[0x04:0x24] & 0xffffffffffffffffffffffffffffffffffffffff;
            var3 = msg.data[0x24:0x44];
            var1 = transfer(var2, var3);
            var temp15 = memory[0x40:0x60];
            memory[temp15:temp15 + 0x20] = !!var1;
            var temp16 = memory[0x40:0x60];
            return memory[temp16:temp16 + (temp15 + 0x20) - temp16];
        } else if (var0 == 0xd41b6db6) {
            // Dispatch table entry for level(address)
            var1 = msg.value;
        
            if (var1) { revert(memory[0x00:0x00]); }
        
            var1 = 0x04bf;
            var2 = msg.data[0x04:0x24] & 0xffffffffffffffffffffffffffffffffffffffff;
            var2 = level(var2);
            var temp17 = memory[0x40:0x60];
            memory[temp17:temp17 + 0x20] = var2;
            var temp18 = memory[0x40:0x60];
            return memory[temp18:temp18 + (temp17 + 0x20) - temp18];
        } else if (var0 == 0xe4d16afc) {
            // Dispatch table entry for 0xe4d16afc (unknown)
            var1 = msg.value;
        
            if (var1) { revert(memory[0x00:0x00]); }
        
            var1 = 0x04ea;
            var2 = func_11F9();
            var temp19 = memory[0x40:0x60];
            memory[temp19:temp19 + 0x20] = !!var2;
            var temp20 = memory[0x40:0x60];
            return memory[temp20:temp20 + (temp19 + 0x20) - temp20];
        } else if (var0 == 0xed21248c) {
            // Dispatch table entry for Deposit()
            var1 = 0x050c;
            Deposit();
            stop();
        } else { revert(memory[0x00:0x00]); }
    }
    
    function func_050E(var arg0) returns (var arg0) {
        memory[0x20:0x40] = 0x05;
        memory[0x00:0x20] = arg0;
        return storage[keccak256(memory[0x00:0x40])];
    }
    
    function revise(var arg0, var arg1) {
        if (storage[0x01] < 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000) { revert(memory[0x00:0x00]); }
    
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x05;
    
        if (storage[keccak256(memory[0x00:0x40])] != 0x02) { revert(memory[0x00:0x00]); }
    
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x06;
    
        if (storage[keccak256(memory[0x00:0x40])] != 0x02) { revert(memory[0x00:0x00]); }
    
        if (!!(storage[0x00] / 0x0100 ** 0x14 & 0xff) != !!0x01) { revert(memory[0x00:0x00]); }
    
        var var0 = arg1;
        var var1 = 0x01;
        var var2 = arg0;
    
        if (var2 >= storage[var1]) { assert(); }
    
        memory[0x00:0x20] = var1;
        storage[keccak256(memory[0x00:0x20]) + var2] = var0;
    
        if (storage[0x01] >= 0xffffffffff000000000000000000000000000000000000000000000000000000) {
            memory[0x00:0x20] = msg.sender;
            memory[0x20:0x40] = 0x06;
            var temp0 = keccak256(memory[0x00:0x40]);
            storage[temp0] = storage[temp0] + 0x01;
            return;
        } else {
            var0 = 0x00;
            var1 = 0x0676;
            var2 = 0x01;
            var var3 = var0;
            func_1489(var2, var3);
            revert(memory[0x00:0x00]);
        }
    }
    
    function func_06CE(var arg0) {
        var var0 = msg.sender;
        var var1 = var0 & 0xffffffffffffffffffffffffffffffffffffffff;
        var var2 = 0xa8286aca;
        var temp0 = memory[0x40:0x60];
        memory[temp0:temp0 + 0x20] = (var2 & 0xffffffff) * 0x0100000000000000000000000000000000000000000000000000000000;
        var temp1 = temp0 + 0x04;
        memory[temp1:temp1 + 0x20] = arg0;
        var var3 = temp1 + 0x20;
        var var4 = 0x20;
        var var5 = memory[0x40:0x60];
        var var6 = var3 - var5;
        var var7 = var5;
        var var8 = 0x00;
        var var9 = var1;
        var var10 = !address(var9).code.length;
    
        if (var10) { revert(memory[0x00:0x00]); }
    
        var temp2;
        temp2, memory[var5:var5 + var4] = address(var9).call.gas(msg.gas).value(var8)(memory[var7:var7 + var6]);
        var4 = !temp2;
    
        if (!var4) {
            var1 = memory[0x40:0x60];
            var2 = returndata.length;
        
            if (var2 < 0x20) { revert(memory[0x00:0x00]); }
        
            if (memory[var1:var1 + 0x20]) {
            label_0850:
                return;
            } else {
                storage[0x03] = arg0;
                var1 = var0 & 0xffffffffffffffffffffffffffffffffffffffff;
                var2 = 0xa8286aca;
                var temp3 = memory[0x40:0x60];
                memory[temp3:temp3 + 0x20] = (var2 & 0xffffffff) * 0x0100000000000000000000000000000000000000000000000000000000;
                var temp4 = temp3 + 0x04;
                memory[temp4:temp4 + 0x20] = storage[0x03];
                var3 = temp4 + 0x20;
                var4 = 0x20;
                var5 = memory[0x40:0x60];
                var6 = var3 - var5;
                var7 = var5;
                var8 = 0x00;
                var9 = var1;
                var10 = !address(var9).code.length;
            
                if (var10) { revert(memory[0x00:0x00]); }
            
                var temp5;
                temp5, memory[var5:var5 + var4] = address(var9).call.gas(msg.gas).value(var8)(memory[var7:var7 + var6]);
                var4 = !temp5;
            
                if (!var4) {
                    var1 = memory[0x40:0x60];
                    var2 = returndata.length;
                
                    if (var2 < 0x20) { revert(memory[0x00:0x00]); }
                
                    storage[0x02] = !!memory[var1:var1 + 0x20] | (storage[0x02] & ~0xff);
                    goto label_0850;
                } else {
                    var temp6 = returndata.length;
                    memory[0x00:0x00 + temp6] = returndata[0x00:0x00 + temp6];
                    revert(memory[0x00:0x00 + returndata.length]);
                }
            }
        } else {
            var temp7 = returndata.length;
            memory[0x00:0x00 + temp7] = returndata[0x00:0x00 + temp7];
            revert(memory[0x00:0x00 + returndata.length]);
        }
    }
    
    function gift() {
        var var0 = address(msg.sender).code.length;
    
        if (var0 != 0x00) { revert(memory[0x00:0x00]); }
    
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x05;
    
        if (storage[keccak256(memory[0x00:0x40])] != 0x00) { revert(memory[0x00:0x00]); }
    
        if (msg.sender & 0x0fff != 0x0111) { revert(memory[0x00:0x00]); }
    
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x04;
        storage[keccak256(memory[0x00:0x40])] = 0x64;
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x05;
        var temp0 = keccak256(memory[0x00:0x40]);
        storage[temp0] = storage[temp0] + 0x01;
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x06;
        var temp1 = keccak256(memory[0x00:0x40]);
        storage[temp1] = storage[temp1] + 0x01;
    }
    
    function withdraw(var arg0) {
        if (msg.sender != storage[0x00] & 0xffffffffffffffffffffffffffffffffffffffff) { revert(memory[0x00:0x00]); }
    
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x05;
    
        if (storage[keccak256(memory[0x00:0x40])] != 0x02) { revert(memory[0x00:0x00]); }
    
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x06;
    
        if (storage[keccak256(memory[0x00:0x40])] != 0x03) { revert(memory[0x00:0x00]); }
    
        if (arg0 < 0x64) { revert(memory[0x00:0x00]); }
    
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x04;
    
        if (storage[keccak256(memory[0x00:0x40])] < arg0) { revert(memory[0x00:0x00]); }
    
        if (address(this).balance < arg0) { revert(memory[0x00:0x00]); }
    
        var temp0 = arg0;
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x04;
        var temp1 = keccak256(memory[0x00:0x40]);
        storage[temp1] = storage[temp1] - temp0; // balance1 = balance1 - arg0

        var temp2 = memory[0x40:0x60];
        memory[temp2:temp2 + 0x00] = address(msg.sender).call.gas(msg.gas).value(temp0)(memory[temp2:temp2 + memory[0x40:0x60] - temp2]);
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x05;
        var temp3 = keccak256(memory[0x00:0x40]);
        storage[temp3] = storage[temp3] - 0x01;
    }
    
    function retract() {
        if (storage[0x01] != 0x00) { revert(memory[0x00:0x00]); }
    
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x05;
    
        if (storage[keccak256(memory[0x00:0x40])] != 0x02) { revert(memory[0x00:0x00]); }
    
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x06;
    
        if (storage[keccak256(memory[0x00:0x40])] != 0x02) { revert(memory[0x00:0x00]); }
    
        if (!!(storage[0x00] / 0x0100 ** 0x14 & 0xff) != !!0x01) { revert(memory[0x00:0x00]); }
    
        var var0 = storage[0x01] - 0x01;
        var var1 = 0x0cf4;
        var var2 = 0x01;
        var var3 = var0;
        func_1489(var2, var3);
    }
    
    function payforflag(var arg0) {
        if (msg.sender != storage[0x00] & 0xffffffffffffffffffffffffffffffffffffffff) { revert(memory[0x00:0x00]); }
    
        if (msg.sender & 0x0fff != 0x0111) { revert(memory[0x00:0x00]); }
    
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x06;
    
        if (storage[keccak256(memory[0x00:0x40])] != 0x03) { revert(memory[0x00:0x00]); }
    
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x05;
    
        if (storage[keccak256(memory[0x00:0x40])] <= 0x8ac7230489e80000) { revert(memory[0x00:0x00]); }
    
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x04;
        storage[keccak256(memory[0x00:0x40])] = 0x00;
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x06;
        storage[keccak256(memory[0x00:0x40])] = 0x00;
        storage[0x02] = (storage[0x02] & ~0xff) | 0x00;
        storage[0x00] = (storage[0x00] & ~(0xff * 0x0100 ** 0x14)) | 0x00;
        var var0 = 0x00;
        var var1 = 0x0eed;
        var var3 = var0;
        var var2 = 0x01;
        func_1489(var2, var3);
        var0 = 0x296b9274d26b7baffb5cc93e1af19012c35ace27ba9acf1badff99d1f76dfa69;
        var temp0 = arg0;
        var1 = temp0;
        var temp1 = memory[0x40:0x60];
        var2 = temp1;
        var3 = var2;
        var temp2 = var3 + 0x20;
        memory[var3:var3 + 0x20] = temp2 - var3;
        memory[temp2:temp2 + 0x20] = memory[var1:var1 + 0x20];
        var var4 = temp2 + 0x20;
        var var6 = memory[var1:var1 + 0x20];
        var var5 = var1 + 0x20;
        var var7 = var6;
        var var8 = var4;
        var var9 = var5;
        var var10 = 0x00;
    
        if (var10 >= var7) {
        label_0F50:
            var temp3 = var6;
            var4 = temp3 + var4;
            var5 = temp3 & 0x1f;
        
            if (!var5) {
                var temp4 = memory[0x40:0x60];
                log(memory[temp4:temp4 + var4 - temp4], [stack[-6]]);
                return;
            } else {
                var temp5 = var5;
                var temp6 = var4 - temp5;
                memory[temp6:temp6 + 0x20] = ~(0x0100 ** (0x20 - temp5) - 0x01) & memory[temp6:temp6 + 0x20];
                var temp7 = memory[0x40:0x60];
                log(memory[temp7:temp7 + (temp6 + 0x20) - temp7], [stack[-6]]);
                return;
            }
        } else {
        label_0F3E:
            var temp8 = var10;
            memory[var8 + temp8:var8 + temp8 + 0x20] = memory[var9 + temp8:var9 + temp8 + 0x20];
            var10 = temp8 + 0x20;
        
            if (var10 >= var7) { goto label_0F50; }
            else { goto label_0F3E; }
        }
    }
    
    function balanceOf(var arg0) returns (var arg0) {
        memory[0x20:0x40] = 0x04;
        memory[0x00:0x20] = arg0;
        return storage[keccak256(memory[0x00:0x40])];
    }
    
    function func_0FA5() returns (var r0) { return storage[0x00] / 0x0100 ** 0x14 & 0xff; }
    
    function owner() returns (var r0) { return storage[0x00] & 0xffffffffffffffffffffffffffffffffffffffff; }
    
    function func_0FDD() returns (var r0) { return storage[0x03]; }
    
    function guess(var arg0) {
        var var1 = 0x00;
        var var0 = block.blockHash(block.number - 0x01);
        var var2 = 0x03;
        var var3 = var0;
    
        if (!var2) { assert(); }
    
        var1 = var3 % var2;
    
        if (var1 != arg0) { return; }
    
        storage[0x00] = (storage[0x00] & ~(0xff * 0x0100 ** 0x14)) | 0x0100 ** 0x14;
    }
    
    function codex(var arg0) returns (var arg0) {
        var var0 = 0x01;
        var var1 = arg0;
    
        if (var1 >= storage[var0]) { assert(); }
    
        memory[0x00:0x20] = var0;
        return storage[keccak256(memory[0x00:0x20]) + var1];
    }
    
    function buy() {
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x06;
    
        if (storage[keccak256(memory[0x00:0x40])] != 0x01) { revert(memory[0x00:0x00]); }
    
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x05;
    
        if (storage[keccak256(memory[0x00:0x40])] != 0x01) { revert(memory[0x00:0x00]); }
    
        if (!!(storage[0x02] & 0xff) != !!0x01) { revert(memory[0x00:0x00]); }
    
        if (!!(storage[0x00] / 0x0100 ** 0x14 & 0xff) != !!0x01) { revert(memory[0x00:0x00]); }
    
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x05;
        var temp0 = keccak256(memory[0x00:0x40]);
        storage[temp0] = storage[temp0] + 0x01;
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x06;
        var temp1 = keccak256(memory[0x00:0x40]);
        storage[temp1] = storage[temp1] + 0x01;
    }
    
    function transfer(var arg0, var arg1) returns (var r0) {
        var var0 = 0x00;
        var var1 = 0x11d7;
        var var2 = msg.sender;
        var var3 = arg0;
        var var4 = arg1;
        func_126F(var2, var3, var4);
        return 0x01;
    }
    
    function level(var arg0) returns (var arg0) {
        memory[0x20:0x40] = 0x06;
        memory[0x00:0x20] = arg0;
        return storage[keccak256(memory[0x00:0x40])];
    }
    
    function func_11F9() returns (var r0) { return storage[0x02] & 0xff; }
    
    function Deposit() {
        if (msg.value < 0x1b1ae4d6e2ef500000) { return; }
    
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x05;
        var temp0 = keccak256(memory[0x00:0x40]);
        storage[temp0] = storage[temp0] + 0x01;
    }
    
    function func_126F(var arg0, var arg1, var arg2) {
        var var0 = 0x00;
        var var1 = var0;
        var var2 = 0x00;
        var var3 = var2;
    
        if (arg1 & 0xffffffffffffffffffffffffffffffffffffffff == 0xffffffffffffffffffffffffffffffffffffffff & 0x00) { revert(memory[0x00:0x00]); }
    
        if (arg2 <= 0x00) { revert(memory[0x00:0x00]); }
    
        var temp0 = arg0;
        memory[0x00:0x20] = temp0 & 0xffffffffffffffffffffffffffffffffffffffff;
        memory[0x20:0x40] = 0x04;
        var temp1 = storage[keccak256(memory[0x00:0x40])];
        var0 = temp1;
        var temp2 = arg1;
        memory[0x00:0x20] = temp2 & 0xffffffffffffffffffffffffffffffffffffffff;
        memory[0x20:0x40] = 0x04;
        var1 = storage[keccak256(memory[0x00:0x40])];
        var temp3 = arg2;
        memory[0x00:0x20] = temp0 & 0xffffffffffffffffffffffffffffffffffffffff;
        memory[0x20:0x40] = 0x04;
        var2 = storage[keccak256(memory[0x00:0x40])] - temp3;
        memory[0x00:0x20] = temp2 & 0xffffffffffffffffffffffffffffffffffffffff;
        memory[0x20:0x40] = 0x04;
        var3 = storage[keccak256(memory[0x00:0x40])] + temp3;
    
        if (var0 < temp3) { revert(memory[0x00:0x00]); }
    
        if (var3 <= var1) { revert(memory[0x00:0x00]); }
    
        var temp4 = var2;
        memory[0x00:0x20] = arg0 & 0xffffffffffffffffffffffffffffffffffffffff;
        memory[0x20:0x40] = 0x04;
        storage[keccak256(memory[0x00:0x40])] = temp4;
        var temp5 = var3;
        memory[0x00:0x20] = arg1 & 0xffffffffffffffffffffffffffffffffffffffff;
        memory[0x20:0x40] = 0x04;
        storage[keccak256(memory[0x00:0x40])] = temp5;
    
        if (var0 + var1 == temp4 + temp5) { return; }
        else { assert(); }
    }
    
    function func_1489(var arg0, var arg1) {
        var temp0 = arg0;
        var temp1 = storage[temp0];
        var var0 = temp1;
        var temp2 = arg1;
        storage[temp0] = temp2;
    
        if (var0 <= temp2) {
        label_14B0:
            return;
        } else {
            memory[0x00:0x20] = arg0;
            var temp3 = keccak256(memory[0x00:0x20]);
            var temp4 = temp3 + var0;
            var0 = 0x14af;
            var var1 = temp4;
            var var2 = temp3 + arg1;
            var0 = func_14B5(var1, var2);
            goto label_14B0;
        }
    }
    
    function func_14B5(var arg0, var arg1) returns (var r0) {
        var temp0 = arg0;
        arg0 = 0x14d7;
        var temp1 = arg1;
        var var0 = temp1;
        arg1 = temp0;
    
        if (arg1 <= var0) { return func_14D3(arg1, var0); }
    
    label_14C4:
        var temp2 = var0;
        storage[temp2] = 0x00;
        var0 = temp2 + 0x01;
    
        if (arg1 > var0) { goto label_14C4; }
    
        arg0 = func_14D3(arg1, var0);
        // Error: Could not resolve method call return address!
    }
    
    function func_14D3(var arg0, var arg1) returns (var r0) { return arg0; }
}


