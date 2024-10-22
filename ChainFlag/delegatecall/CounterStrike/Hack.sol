pragma solidity ^0.8.11;

import "console.sol";

contract Hack {
    address target;

    constructor(address _target){
        address easybomb = target.call(abi.encodeWithSignature("easyBomb()"));

    }

    function run() public{
        bool success;
        bytes memory result;
    }
}


contract Deploy {
    constructor(address _target) payable {
        Hack h = new Hack(_target)
    }
}


